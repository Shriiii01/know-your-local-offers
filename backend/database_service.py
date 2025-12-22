"""
Database Service for Know Your Local Offers
Handles all database operations for offers, cities, and categories
"""
from supabase_client import supabase
from typing import List, Dict, Optional
import asyncio
import re

class DatabaseService:
    def __init__(self):
        self.supabase = supabase
    
    async def search_offers(self, query: str = "", city: str = None, category: str = None, limit: int = 10) -> List[Dict]:
        """Search for offers based on user query with intelligent filtering"""
        try:
            # Build the base query
            db_query = self.supabase.table("offers").select("*")
            
            # Apply filters
            if city:
                db_query = db_query.ilike("city", f"%{city}%")
            
            if category:
                db_query = db_query.eq("category", category)
            
            # Search in multiple fields if query is provided
            if query and query.strip():
                # Clean the query
                clean_query = query.strip().lower()
                db_query = db_query.or_(
                    f"offer_text.ilike.%{clean_query}%,"
                    f"store_name.ilike.%{clean_query}%,"
                    f"category.ilike.%{clean_query}%"
                )
            
            # Add limit and order by validity
            db_query = db_query.order("valid_till", desc=False).limit(limit)
            
            # Execute query
            result = db_query.execute()
            return result.data if result.data else []
            
        except Exception as e:
            print(f"[DatabaseService] Search error: {e}")
            return []
    
    async def get_offers_by_city(self, city: str, limit: int = 10) -> List[Dict]:
        """Get all offers for a specific city"""
        try:
            result = (self.supabase.table("offers")
                     .select("*")
                     .ilike("city", f"%{city}%")
                     .order("valid_till", desc=False)
                     .limit(limit)
                     .execute())
            return result.data if result.data else []
        except Exception as e:
            print(f"[DatabaseService] City search error: {e}")
            return []
    
    async def get_offers_by_category(self, category: str, limit: int = 10) -> List[Dict]:
        """Get all offers for a specific category"""
        try:
            result = (self.supabase.table("offers")
                     .select("*")
                     .eq("category", category)
                     .order("valid_till", desc=False)
                     .limit(limit)
                     .execute())
            return result.data if result.data else []
        except Exception as e:
            print(f"[DatabaseService] Category search error: {e}")
            return []
    
    async def get_trending_offers(self, limit: int = 5) -> List[Dict]:
        """Get trending/popular offers"""
        try:
            result = (self.supabase.table("offers")
                     .select("*")
                     .order("valid_till", desc=False)
                     .limit(limit)
                     .execute())
            return result.data if result.data else []
        except Exception as e:
            print(f"[DatabaseService] Trending offers error: {e}")
            return []
    
    async def get_offers_by_price_range(self, min_price: int = None, max_price: int = None) -> List[Dict]:
        """Get offers within a specific price range"""
        try:
            # This is a simplified version - you might need to adjust based on your price_range field format
            query = self.supabase.table("offers").select("*")
            
            # For now, we'll search in price_range text field
            # You could enhance this by parsing the price_range field
            if min_price:
                query = query.gte("price_range", f"₹{min_price}")
            if max_price:
                query = query.lte("price_range", f"₹{max_price}")
            
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"[DatabaseService] Price range search error: {e}")
            return []
    
    async def add_offer(self, offer_data: Dict) -> bool:
        """Add a new offer to the database"""
        try:
            required_fields = ["store_name", "city", "category", "offer_text"]
            if not all(field in offer_data for field in required_fields):
                print("[DatabaseService] Missing required fields for new offer")
                return False
            
            result = self.supabase.table("offers").insert(offer_data).execute()
            return bool(result.data)
        except Exception as e:
            print(f"[DatabaseService] Add offer error: {e}")
            return False
    
    async def get_cities(self) -> List[str]:
        """Get list of all cities with offers"""
        try:
            result = (self.supabase.table("offers")
                     .select("city")
                     .execute())
            if result.data:
                cities = list(set(item["city"] for item in result.data if item.get("city")))
                return sorted(cities)
            return []
        except Exception as e:
            print(f"[DatabaseService] Get cities error: {e}")
            return []
    
    async def get_categories(self) -> List[str]:
        """Get list of all categories with offers"""
        try:
            result = (self.supabase.table("offers")
                     .select("category")
                     .execute())
            if result.data:
                categories = list(set(item["category"] for item in result.data if item.get("category")))
                return sorted(categories)
            return []
        except Exception as e:
            print(f"[DatabaseService] Get categories error: {e}")
            return []