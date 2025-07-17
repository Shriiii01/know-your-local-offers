import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import json
import os
from urllib.parse import urljoin, urlparse
import logging
from typing import List, Dict, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JustdialScraper:
    def __init__(self):
        self.base_url = "https://www.justdial.com"
        self.session = requests.Session()
        
        # Enhanced headers to mimic a real browser better
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/'
        })
        
        # Add session configuration
        self.session.max_redirects = 10
        
        # CSV columns  
        self.csv_columns = ['name', 'address', 'phone', 'opening_hours', 'image_url', 'rating', 'website']
        
    def decode_phone_number(self, encoded_phone: str) -> str:
        """
        Decode Justdial's encoded phone numbers.
        This is a simplified decoder - Justdial uses various encoding methods.
        """
        if not encoded_phone:
            return ""
        
        # Try to find patterns in the encoded phone
        # Method 1: Look for data-phone attributes
        phone_pattern = r'data-phone[^>]*?([0-9\-\+\(\)\s]+)'
        match = re.search(phone_pattern, encoded_phone)
        if match:
            return match.group(1).strip()
            
        # Method 2: Look for tel: links
        tel_pattern = r'tel:([0-9\+\-\(\)\s]+)'
        match = re.search(tel_pattern, encoded_phone)
        if match:
            return match.group(1).strip()
            
        # Method 3: Extract any phone-like pattern
        phone_digits = re.findall(r'[0-9\+\-\(\)\s]{10,}', encoded_phone)
        if phone_digits:
            return phone_digits[0].strip()
            
        return ""
    
    def extract_shop_details(self, shop_element) -> Dict[str, str]:
        """Extract details from a single shop element"""
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
            # Extract name - try multiple selectors for current Justdial structure
            name_selectors = [
                'h2.jcn a',
                '.jcn h2 a', 
                '.resultbox_title_anchor',
                '.store-name',
                'h2 a[title]',
                '.fn.jcn a',
                '.fn.jcn',
                '.jcn a',
                '.jcn',
                '.companyname a',
                '[data-name]'
            ]
            
            for selector in name_selectors:
                name_elem = shop_element.select_one(selector)
                if name_elem:
                    name_text = name_elem.get_text(strip=True) or name_elem.get('title', '').strip()
                    if name_text and len(name_text) > 2:
                        details['name'] = name_text
                        break
            
            # Extract address - enhanced selectors
            address_selectors = [
                '.store-addr',
                '.resultbox_address',
                '.companyaddress', 
                '.lng.jcn',
                '.loc.jcn.lng',
                '.loc',
                '.adr',
                '.address-text'
            ]
            
            for selector in address_selectors:
                addr_elem = shop_element.select_one(selector)
                if addr_elem:
                    addr_text = addr_elem.get_text(strip=True)
                    if addr_text and len(addr_text) > 5:
                        details['address'] = addr_text
                        break
            
            # Extract phone number - comprehensive approach
            phone_selectors = [
                'a[href*="tel:"]',
                '[data-phone]',
                '.tel.jcn',
                '.mobilesv',
                '.tele.jcn',
                '.phone-container',
                '.contact-info'
            ]
            
            phone_found = False
            for selector in phone_selectors:
                phone_elem = shop_element.select_one(selector)
                if phone_elem and not phone_found:
                    if phone_elem.has_attr('data-phone'):
                        phone = phone_elem['data-phone']
                    elif phone_elem.has_attr('href') and 'tel:' in phone_elem['href']:
                        phone = phone_elem['href'].replace('tel:', '')
                    else:
                        phone = phone_elem.get_text(strip=True)
                    
                    # Clean and validate phone number
                    if phone:
                        # Remove non-digits except +
                        cleaned_phone = re.sub(r'[^\d+]', '', phone)
                        # Look for Indian phone patterns
                        if re.match(r'^(\+91)?[6-9]\d{9}$', cleaned_phone.replace('+91', '')):
                            details['phone'] = cleaned_phone.replace('+91', '')
                            phone_found = True
                            break
            
            # Try to decode phone if it's encoded
            if not phone_found and details.get('phone'):
                decoded_phone = self.decode_phone_number(str(shop_element))
                if decoded_phone:
                    details['phone'] = decoded_phone
            
            # Extract opening hours
            hours_selectors = [
                '.hours-info',
                '.timing',
                '.working-hours',
                '.store-timing', 
                '.timings',
                '.hrs',
                '.hours',
                '.opening-hours'
            ]
            
            for selector in hours_selectors:
                hours_elem = shop_element.select_one(selector)
                if hours_elem:
                    hours_text = hours_elem.get_text(strip=True)
                    if hours_text and ('AM' in hours_text or 'PM' in hours_text or 'open' in hours_text.lower()):
                        details['opening_hours'] = hours_text
                        break
            
            # Extract rating
            rating_selectors = [
                '.rating-value',
                '.store-rating',
                '.rating .number',
                '[data-rating]',
                '.star-rating'
            ]
            
            for selector in rating_selectors:
                rating_elem = shop_element.select_one(selector)
                if rating_elem:
                    rating_text = rating_elem.get_text(strip=True) or rating_elem.get('data-rating', '')
                    if rating_text and any(c.isdigit() for c in rating_text):
                        details['rating'] = rating_text
                        break
            
            # Extract image URL - enhanced
            img_selectors = [
                'img[data-src]',
                'img[src]:not([src*="data:"])',
                '.store-img img',
                '.company-logo img'
            ]
            
            for selector in img_selectors:
                img_elem = shop_element.select_one(selector)
                if img_elem:
                    img_src = img_elem.get('data-src') or img_elem.get('src')
                    if img_src and not img_src.startswith('data:') and 'logo' not in img_src.lower():
                        full_url = urljoin(self.base_url, img_src)
                        details['image_url'] = full_url
                        break
            
            # Extract website
            website_elem = shop_element.select_one('a[href*="http"]:not([href*="justdial"])')
            if website_elem:
                website_url = website_elem.get('href', '')
                if website_url and 'justdial' not in website_url:
                    details['website'] = website_url
            
        except Exception as e:
            logger.error(f"Error extracting shop details: {e}")
        
        return details
    
    def scrape_page(self, url: str) -> List[Dict[str, str]]:
        """Scrape a single page for shop details"""
        logger.info(f"Scraping page: {url}")
        
        try:
            # Try multiple times with different timeouts
            for attempt in range(3):
                try:
                    timeout = 20 + (attempt * 10)  # Progressive timeout
                    logger.info(f"Attempt {attempt + 1} with timeout {timeout}s")
                    
                    response = self.session.get(url, timeout=timeout)
                    response.raise_for_status()
                    
                    if response.status_code == 200:
                        break
                        
                except requests.Timeout:
                    logger.warning(f"Timeout on attempt {attempt + 1}")
                    if attempt == 2:
                        raise
                    time.sleep(5)
                    continue
                except requests.RequestException as e:
                    logger.warning(f"Request error on attempt {attempt + 1}: {e}")
                    if attempt == 2:
                        raise
                    time.sleep(5)
                    continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            shops = []
            
            # Enhanced selectors for Justdial's current structure
            shop_selectors = [
                '.resultbox',
                '.store-details',
                '.resultbox_textdetail',
                '.result-list .result',
                '.comp-list .comp',
                '.resultsData .result',
                '.jcn-listing .jcn-block',
                '.listing-item'
            ]
            
            shop_elements = []
            for selector in shop_selectors:
                elements = soup.select(selector)
                if elements:
                    logger.info(f"Found {len(elements)} elements using selector: {selector}")
                    shop_elements = elements
                    break
            
            if not shop_elements:
                # Fallback: look for any element with business-like classes
                fallback_selectors = [
                    'div[class*="result"]',
                    'div[class*="comp"]', 
                    'div[class*="list"]',
                    'div[class*="store"]',
                    'div[class*="jcn"]'
                ]
                
                for selector in fallback_selectors:
                    elements = soup.select(selector)
                    if elements:
                        logger.info(f"Fallback: found {len(elements)} elements with selector: {selector}")
                        shop_elements = elements
                        break
            
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
        """Find the next page URL"""
        
        # Try different selectors for next page links
        next_selectors = [
            'a[title*="Next"]',
            'a[rel="next"]',
            '.next',
            '.pagination a[title*="Next"]',
            '.page-next',
            'a:contains("Next")'
        ]
        
        for selector in next_selectors:
            try:
                next_elem = soup.select_one(selector)
                if next_elem and next_elem.get('href'):
                    next_url = urljoin(self.base_url, next_elem['href'])
                    return next_url
            except:
                continue
        
        # Look for pagination links with numbers
        pagination_links = soup.select('.pagination a, .page-links a')
        for link in pagination_links:
            if link.get_text(strip=True).isdigit():
                href = link.get('href')
                if href:
                    return urljoin(self.base_url, href)
        
        return None
    
    def scrape_all_pages(self, start_url: str, max_pages: int = 50) -> List[Dict[str, str]]:
        """Scrape all pages starting from the given URL"""
        all_shops = []
        current_url = start_url
        page_count = 0
        
        while current_url and page_count < max_pages:
            page_count += 1
            logger.info(f"Scraping page {page_count}: {current_url}")
            
            # Get page content
            try:
                response = self.session.get(current_url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
            except Exception as e:
                logger.error(f"Failed to get page {page_count}: {e}")
                break
            
            # Extract shops from current page
            page_shops = self.scrape_page(current_url)
            all_shops.extend(page_shops)
            
            # Get next page URL
            next_url = self.get_next_page_url(soup, current_url)
            
            if next_url and next_url != current_url:
                current_url = next_url
                time.sleep(2)  # Be respectful to the server
            else:
                logger.info("No more pages found or reached the end")
                break
        
        logger.info(f"Scraped {page_count} pages, found {len(all_shops)} shops total")
        return all_shops
    
    def save_to_csv(self, shops: List[Dict[str, str]], filename: str = None):
        """Save shops data to CSV file"""
        if not shops:
            logger.warning("No shops data to save")
            return
        
        if filename is None:
            filename = os.path.join('..', 'data', 'kolhapur_jewelry_shops_justdial.csv')
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
                writer.writeheader()
                writer.writerows(shops)
            
            logger.info(f"Successfully saved {len(shops)} shops to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    def run_scraper(self, start_url: str = "https://www.justdial.com/Kolhapur/Jewellery-Shops/nct-10282098"):
        """Main method to run the scraper"""
        logger.info("Starting Justdial scraper for Kolhapur jewelry shops")
        logger.info(f"Starting URL: {start_url}")
        
        # Scrape all pages
        all_shops = self.scrape_all_pages(start_url)
        
        # Remove duplicates based on name and address
        unique_shops = []
        seen = set()
        
        for shop in all_shops:
            key = (shop['name'].lower().strip(), shop['address'].lower().strip())
            if key not in seen and shop['name']:
                seen.add(key)
                unique_shops.append(shop)
        
        logger.info(f"Found {len(all_shops)} total shops, {len(unique_shops)} unique shops")
        
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
        print(f"Shops with websites: {len([s for s in unique_shops if s['website']])}")
        print(f"{'='*60}")
        
        return unique_shops

def main():
    """Main function to run the scraper"""
    scraper = JustdialScraper()
    shops = scraper.run_scraper()
    
    # Print first few shops as example
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