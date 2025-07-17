import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import json
import os
from urllib.parse import urljoin, urlparse, parse_qs
import logging
from typing import List, Dict, Optional
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedJustdialScraper:
    def __init__(self):
        self.base_url = "https://www.justdial.com"
        self.session = requests.Session()
        
        # Enhanced headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })
        
        # CSV columns
        self.csv_columns = ['name', 'address', 'phone', 'opening_hours', 'image_url', 'rating', 'website']
        
    def extract_phone_from_onclick(self, onclick_text: str) -> str:
        """Extract phone number from onclick JavaScript"""
        if not onclick_text:
            return ""
        
        # Look for phone numbers in onclick events
        patterns = [
            r"'(\+?[0-9\-\(\)\s]{10,})'",
            r'"(\+?[0-9\-\(\)\s]{10,})"',
            r'(\+?91[0-9]{10})',
            r'([0-9]{10})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, onclick_text)
            if match:
                phone = match.group(1).strip()
                if len(re.findall(r'\d', phone)) >= 10:
                    return phone
        
        return ""
    
    def clean_phone_number(self, phone: str) -> str:
        """Clean and format phone number"""
        if not phone:
            return ""
        
        # Remove common prefixes and clean
        phone = re.sub(r'^(\+91|91)', '', phone.strip())
        phone = re.sub(r'[^\d]', '', phone)
        
        # Validate Indian phone number
        if len(phone) == 10 and phone[0] in '6789':
            return phone
        elif len(phone) == 11 and phone.startswith('0'):
            return phone[1:]
        
        return phone if len(phone) >= 10 else ""
    
    def extract_shop_details(self, shop_element) -> Dict[str, str]:
        """Enhanced extraction method with multiple fallbacks"""
        details = {
            'name': '',
            'address': '',
            'phone': '',
            'opening_hours': '',
            'image_url': '',
            'rating': '',
            'website': ''
        }
        
        try:
            # Extract name - try multiple selectors
            name_selectors = [
                'h2.jcn a',
                '.jcn h2 a',
                '.resultbox_title_anchor',
                '.store-name',
                'h2 a[title]',
                '.companyname a',
                '[data-name]'
            ]
            
            for selector in name_selectors:
                name_elem = shop_element.select_one(selector)
                if name_elem:
                    details['name'] = name_elem.get_text(strip=True) or name_elem.get('title', '').strip()
                    if details['name']:
                        break
            
            # Extract address
            address_selectors = [
                '.store-addr',
                '.resultbox_address',
                '.companyaddress',
                '.lng.jcn',
                '.address-text',
                '.adr'
            ]
            
            for selector in address_selectors:
                addr_elem = shop_element.select_one(selector)
                if addr_elem:
                    details['address'] = addr_elem.get_text(strip=True)
                    if details['address']:
                        break
            
            # Extract phone number - enhanced approach
            phone_found = False
            
            # Method 1: Look for tel: links
            tel_links = shop_element.select('a[href*="tel:"]')
            for link in tel_links:
                href = link.get('href', '')
                if 'tel:' in href:
                    phone = href.replace('tel:', '').strip()
                    cleaned_phone = self.clean_phone_number(phone)
                    if cleaned_phone:
                        details['phone'] = cleaned_phone
                        phone_found = True
                        break
            
            # Method 2: Look for data-phone attributes
            if not phone_found:
                phone_elem = shop_element.select_one('[data-phone]')
                if phone_elem:
                    phone = phone_elem.get('data-phone', '')
                    cleaned_phone = self.clean_phone_number(phone)
                    if cleaned_phone:
                        details['phone'] = cleaned_phone
                        phone_found = True
            
            # Method 3: Look for onclick events with phone numbers
            if not phone_found:
                onclick_elems = shop_element.select('[onclick*="phone"], [onclick*="call"], [onclick*="tel"]')
                for elem in onclick_elems:
                    onclick = elem.get('onclick', '')
                    phone = self.extract_phone_from_onclick(onclick)
                    if phone:
                        cleaned_phone = self.clean_phone_number(phone)
                        if cleaned_phone:
                            details['phone'] = cleaned_phone
                            phone_found = True
                            break
            
            # Method 4: Look in common phone containers
            if not phone_found:
                phone_containers = shop_element.select('.phone-container, .contact-info, .mobilesv, .tel')
                for container in phone_containers:
                    text = container.get_text(strip=True)
                    phone_match = re.search(r'(\+?91?[6-9]\d{9})', text)
                    if phone_match:
                        phone = phone_match.group(1)
                        cleaned_phone = self.clean_phone_number(phone)
                        if cleaned_phone:
                            details['phone'] = cleaned_phone
                            break
            
            # Extract opening hours
            hours_selectors = [
                '.hours-info',
                '.timing',
                '.working-hours',
                '.store-timing',
                '.opening-hours'
            ]
            
            for selector in hours_selectors:
                hours_elem = shop_element.select_one(selector)
                if hours_elem:
                    details['opening_hours'] = hours_elem.get_text(strip=True)
                    if details['opening_hours']:
                        break
            
            # Extract rating
            rating_selectors = [
                '.rating-value',
                '.store-rating',
                '.rating .number',
                '[data-rating]'
            ]
            
            for selector in rating_selectors:
                rating_elem = shop_element.select_one(selector)
                if rating_elem:
                    rating_text = rating_elem.get_text(strip=True) or rating_elem.get('data-rating', '')
                    if rating_text:
                        details['rating'] = rating_text
                        break
            
            # Extract image URL
            img_selectors = [
                'img[src*="jdlogo"]',
                '.store-img img',
                '.company-logo img',
                'img[data-src]',
                'img[src]'
            ]
            
            for selector in img_selectors:
                img_elem = shop_element.select_one(selector)
                if img_elem:
                    img_src = img_elem.get('data-src') or img_elem.get('src')
                    if img_src and not img_src.startswith('data:'):
                        details['image_url'] = urljoin(self.base_url, img_src)
                        break
            
            # Extract website
            website_elem = shop_element.select_one('a[href*="http"]:not([href*="justdial"])')
            if website_elem:
                details['website'] = website_elem.get('href', '')
            
        except Exception as e:
            logger.error(f"Error extracting shop details: {e}")
        
        return details
    
    def scrape_page(self, url: str) -> List[Dict[str, str]]:
        """Enhanced page scraping with better error handling"""
        logger.info(f"Scraping page: {url}")
        
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            shops = []
            
            # Enhanced selectors for Justdial's current structure
            shop_selectors = [
                '.resultbox',
                '.store-details',
                '.resultbox_textdetail',
                '.result',
                '.comp-details',
                '.listing-item',
                '.jcn-item'
            ]
            
            shop_elements = []
            for selector in shop_selectors:
                elements = soup.select(selector)
                if elements:
                    logger.info(f"Found {len(elements)} elements with selector: {selector}")
                    shop_elements = elements
                    break
            
            # If no specific selectors work, try generic approach
            if not shop_elements:
                # Look for containers that likely contain business info
                potential_containers = soup.select('div[class*="result"], div[class*="store"], div[class*="list"], div[class*="comp"]')
                logger.info(f"Fallback: found {len(potential_containers)} potential containers")
                shop_elements = potential_containers
            
            # Extract details from each element
            for i, shop_elem in enumerate(shop_elements):
                try:
                    shop_details = self.extract_shop_details(shop_elem)
                    if shop_details['name'] and len(shop_details['name']) > 2:
                        shops.append(shop_details)
                        logger.debug(f"Extracted shop {i+1}: {shop_details['name']}")
                except Exception as e:
                    logger.error(f"Error processing shop element {i+1}: {e}")
                    continue
            
            logger.info(f"Successfully extracted {len(shops)} shops from page")
            return shops
            
        except requests.RequestException as e:
            logger.error(f"Request error for {url}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return []
    
    def get_next_page_url(self, soup: BeautifulSoup, current_url: str) -> Optional[str]:
        """Enhanced pagination detection"""
        
        # Try different approaches for pagination
        next_selectors = [
            'a[title*="Next"]',
            'a[rel="next"]',
            '.pagination .next',
            '.page-next a',
            'a:contains("Next")',
            'a[href*="start="]'
        ]
        
        for selector in next_selectors:
            try:
                next_elem = soup.select_one(selector)
                if next_elem and next_elem.get('href'):
                    next_url = urljoin(self.base_url, next_elem['href'])
                    if next_url != current_url:
                        return next_url
            except:
                continue
        
        # Look for numbered pagination
        pagination_links = soup.select('a[href*="start="], .pagination a')
        current_start = 0
        
        # Extract current start parameter
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)
        if 'start' in query_params:
            try:
                current_start = int(query_params['start'][0])
            except:
                current_start = 0
        
        # Look for next page based on start parameter
        for link in pagination_links:
            href = link.get('href')
            if href:
                link_parsed = urlparse(href)
                link_params = parse_qs(link_parsed.query)
                if 'start' in link_params:
                    try:
                        link_start = int(link_params['start'][0])
                        if link_start > current_start:
                            return urljoin(self.base_url, href)
                    except:
                        continue
        
        return None
    
    def scrape_all_pages(self, start_url: str, max_pages: int = 50) -> List[Dict[str, str]]:
        """Enhanced scraping with better progress tracking"""
        all_shops = []
        current_url = start_url
        page_count = 0
        consecutive_empty_pages = 0
        
        while current_url and page_count < max_pages and consecutive_empty_pages < 3:
            page_count += 1
            logger.info(f"Scraping page {page_count}/{max_pages}: {current_url}")
            
            # Get page content
            try:
                response = self.session.get(current_url, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                logger.error(f"Failed to get page {page_count}: {e}")
                consecutive_empty_pages += 1
                break
            
            # Extract shops from current page
            page_shops = self.scrape_page(current_url)
            
            if page_shops:
                all_shops.extend(page_shops)
                consecutive_empty_pages = 0
                logger.info(f"Page {page_count}: Found {len(page_shops)} shops (Total: {len(all_shops)})")
            else:
                consecutive_empty_pages += 1
                logger.warning(f"Page {page_count}: No shops found")
            
            # Get next page URL
            next_url = self.get_next_page_url(soup, current_url)
            
            if next_url and next_url != current_url:
                current_url = next_url
                time.sleep(2)  # Be respectful
            else:
                logger.info("No more pages found")
                break
        
        logger.info(f"Scraping complete: {page_count} pages, {len(all_shops)} total shops")
        return all_shops
    
    def save_to_csv(self, shops: List[Dict[str, str]], filename: str = None):
        """Enhanced CSV saving with better error handling"""
        if not shops:
            logger.warning("No shops data to save")
            return
        
        if filename is None:
            filename = os.path.join('..', 'data', 'kolhapur_jewelry_shops_justdial_enhanced.csv')
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
                writer.writeheader()
                writer.writerows(shops)
            
            logger.info(f"Successfully saved {len(shops)} shops to {filename}")
            print(f"Data saved to: {filename}")
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    def run_scraper(self, start_url: str = "https://www.justdial.com/Kolhapur/Jewellery-Shops/nct-10282098"):
        """Enhanced main scraping method"""
        logger.info("Starting Enhanced Justdial scraper for Kolhapur jewelry shops")
        logger.info(f"Starting URL: {start_url}")
        
        # Test the URL first
        try:
            test_response = self.session.get(start_url, timeout=15)
            test_response.raise_for_status()
            logger.info("Successfully connected to Justdial")
        except Exception as e:
            logger.error(f"Failed to connect to starting URL: {e}")
            return []
        
        # Scrape all pages
        all_shops = self.scrape_all_pages(start_url)
        
        # Remove duplicates
        unique_shops = []
        seen = set()
        
        for shop in all_shops:
            if not shop['name']:
                continue
                
            # Create a unique key
            key = (shop['name'].lower().strip(), shop['address'].lower().strip()[:50])
            if key not in seen:
                seen.add(key)
                unique_shops.append(shop)
        
        logger.info(f"Deduplication: {len(all_shops)} -> {len(unique_shops)} unique shops")
        
        # Save to CSV
        self.save_to_csv(unique_shops)
        
        # Print detailed summary
        print(f"\n{'='*60}")
        print("SCRAPING SUMMARY")
        print(f"{'='*60}")
        print(f"Total shops found: {len(all_shops)}")
        print(f"Unique shops: {len(unique_shops)}")
        print(f"Shops with phone numbers: {len([s for s in unique_shops if s['phone']])}")
        print(f"Shops with addresses: {len([s for s in unique_shops if s['address']])}")
        print(f"Shops with images: {len([s for s in unique_shops if s['image_url']])}")
        print(f"Shops with opening hours: {len([s for s in unique_shops if s['opening_hours']])}")
        print(f"Shops with ratings: {len([s for s in unique_shops if s['rating']])}")
        print(f"{'='*60}")
        
        return unique_shops

def main():
    """Main function"""
    scraper = EnhancedJustdialScraper()
    shops = scraper.run_scraper()
    
    # Display sample results
    if shops:
        print(f"\nSample Results (First 5 shops):")
        print("-" * 80)
        for i, shop in enumerate(shops[:5], 1):
            print(f"\n{i}. {shop['name']}")
            print(f"   Address: {shop['address']}")
            print(f"   Phone: {shop['phone']}")
            print(f"   Hours: {shop['opening_hours']}")
            print(f"   Rating: {shop['rating']}")
            print(f"   Image: {shop['image_url'][:60] + '...' if len(shop['image_url']) > 60 else shop['image_url']}")
            print(f"   Website: {shop['website']}")
    else:
        print("No shops were extracted. Please check the website structure or connection.")

if __name__ == "__main__":
    main() 