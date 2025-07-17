import os
from openai import OpenAI
from typing import Dict, List
import re
import asyncio

class ChatHandler:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Import here to avoid circular imports
        from database_service import DatabaseService
        self.db_service = DatabaseService()
        
        self.system_prompts: Dict[str, str] = {
            "en": (
                "You are a local offers and deals assistant. You have access to a database of local offers and deals.\n"
                "Your ONLY purpose is to help users find the best offers and deals in their local area.\n"
                "Format offer responses clearly with store name, offer details, price range, and validity.\n"
                "Provide recommendations on which offers are best based on price, location, and value.\n"
                "Be friendly, helpful, and focus exclusively on shopping deals and offers.\n"
                "If asked about anything other than offers, redirect them to ask about local deals."
            ),
        }

    async def generate_reply(self, text: str, language: str = "en") -> str:
        """Generate intelligent reply based on user query - ONLY for offers"""
        try:
            # Only handle offers-related queries
            if self._is_offers_query(text, language):
                return await self._handle_offers_query(text, language)
            
            # Redirect non-offers queries
            return "I specialize in local offers and deals only. Please ask me about offers in your city, like 'gold offers in Kolhapur' or 'jewelry discounts in your area'."
            
        except Exception as e:
            print(f"[ChatHandler] Error in generate_reply: {e}")
            return "Sorry, there was a technical issue. Please try again with an offers query."
    
    def _is_offers_query(self, text: str, language: str) -> bool:
        """Detect if the query is about offers/deals"""
        offer_keywords_en = [
            "offer", "offers", "deal", "deals", "discount", "discounts", "sale", "sales", 
            "price", "prices", "cheap", "store", "stores", "shop", "shops", 
            "jewellery", "jewelry", "gold", "diamond", "bangles", "rings", "buy",
            "purchase", "shopping", "mall", "market", "latest", "best", "available",
            "near", "local", "area", "city"
        ]
        text_lower = text.lower()
        
        # Check for offer-related keywords
        if any(keyword in text_lower for keyword in offer_keywords_en):
            return True
        
        # Check for location mentions (cities)
        cities = ["kolhapur", "sangli", "pune", "mumbai"]
        if any(city in text_lower for city in cities):
            return True
        
        # Check for shopping-related terms
        shopping_terms = ["what", "where", "show", "find", "get", "any", "available"]
        if any(term in text_lower for term in shopping_terms):
            return True
            
        return False
    
    async def _handle_offers_query(self, text: str, language: str) -> str:
        """Handle offers-related queries with database integration"""
        try:
            # Extract search parameters
            city = self._extract_city(text)
            category = self._extract_category(text)
            
            # Search for relevant offers
            offers = await self._search_offers_intelligently(text, city, category)
            
            if offers:
                # Generate intelligent response with offers
                return await self._generate_offers_response(text, offers, language)
            else:
                # No offers found - provide helpful alternative response
                return await self._generate_no_offers_response(city, category, language)
                
        except Exception as e:
            print(f"[ChatHandler] Offers query error: {e}")
            return "There was an issue retrieving offers. Please try again later."
    

    
    async def _search_offers_intelligently(self, text: str, city: str, category: str) -> List[Dict]:
        """Intelligently search for offers based on query"""
        # Don't pass non-English text to search, use extracted parameters instead
        search_query = ""
        if not any(ord(char) > 127 for char in text):  # Only if text is English
            search_query = text
        
        # Try specific search first
        offers = await self.db_service.search_offers(search_query, city, category, limit=5)
        
        if not offers and city:
            # Try city-based search
            offers = await self.db_service.get_offers_by_city(city, limit=5)
        
        if not offers and category:
            # Try category-based search
            offers = await self.db_service.get_offers_by_category(category, limit=5)
        
        if not offers:
            # Get trending offers as fallback
            offers = await self.db_service.get_trending_offers(limit=3)
        
        return offers
    
    async def _generate_offers_response(self, query: str, offers: List[Dict], language: str) -> str:
        """Generate intelligent response with offers data"""
        if not offers:
            return await self._generate_no_offers_response(None, None, language)
        
        offers_text = self._format_offers_for_display(offers)
        
        system_prompt = "You are a local offers specialist. Analyze the available offers and recommend the best deals based on value, location, and user needs. Focus only on shopping offers and deals."
        
        user_prompt = f"""
        User Query: "{query}"
        
        Available Offers from Database:
        {offers_text}
        
        IMPORTANT: Use the exact offers provided above. Analyze and recommend the best deals based on:
        - Value for money
        - Location convenience 
        - Offer validity
        - Price range suitability
        
        Respond in English with clear recommendations about which offers provide the best value.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    
    async def _generate_no_offers_response(self, city: str, category: str, language: str) -> str:
        """Generate helpful response when no offers are found"""
        # Get available cities and categories for suggestions
        available_cities = await self.db_service.get_cities()
        available_categories = await self.db_service.get_categories()
        
        response = "Sorry, no offers match your current search criteria.\n\n"
        if available_cities:
            response += f"Available cities: {', '.join(available_cities)}\n"
        if available_categories:
            response += f"Available categories: {', '.join(available_categories)}\n"
        response += "\nPlease try modifying your search criteria."
        
        return response
    
    def _extract_city(self, text: str) -> str:
        """Extract city from user query"""
        city_mapping = {
            "kolhapur": "Kolhapur",
            "sangli": "Sangli", 
            "pune": "Pune",
            "mumbai": "Mumbai"
        }
        
        text_lower = text.lower()
        for key, value in city_mapping.items():
            if key in text_lower:
                return value
        return None
    
    def _extract_category(self, text: str) -> str:
        """Extract category from user query"""
        category_keywords = {
            "jewellery": ["jewellery", "jewelry", "gold", "diamond", "bangles", "rings", "necklace", "silver"]
        }
        
        text_lower = text.lower()
        for category, keywords in category_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        return None
    
    def _format_offers_for_display(self, offers: List[Dict]) -> str:
        """Format offers for LLM processing"""
        if not offers:
            return "No offers available."
        
        formatted = []
        for i, offer in enumerate(offers, 1):
            formatted.append(f"""
{i}. {offer.get('store_name', 'Unknown Store')} - {offer.get('city', 'Unknown City')}
   Offer: {offer.get('offer_text', 'No details')}
   Price Range: {offer.get('price_range', 'Not specified')}
   Valid Till: {offer.get('valid_till', 'Not specified')}
   Category: {offer.get('category', 'General')}
            """.strip())
        
        return "\n\n".join(formatted)