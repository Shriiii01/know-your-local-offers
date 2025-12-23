"""
Insert Offers Script
Utility script to insert sample jewelry offers into the database
"""
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

jewellery_offers = [
    {
        "store_name": "Shri Jewellers",
        "city": "Kolhapur",
        "category": "jewellery",
        "offer_text": "15% off on gold bangles",
        "price_range": "₹10,000–₹50,000",
        "valid_till": "2025-06-30",
        "source": "walk-in"
    },
    {
        "store_name": "Rajlaxmi Gold",
        "city": "Sangli",
        "category": "jewellery",
        "offer_text": "No making charges on wedding sets",
        "price_range": "₹25,000–₹1,00,000",
        "valid_till": "2025-07-10",
        "source": "newspaper"
    },
    {
        "store_name": "Kalyan Jewellers",
        "city": "Kolhapur",
        "category": "jewellery",
        "offer_text": "Buy gold worth ₹50K, get ₹2K off",
        "price_range": "₹50,000+",
        "valid_till": "2025-07-01",
        "source": "local ad"
    },
    {
        "store_name": "Tanisq Kolhapur",
        "city": "Kolhapur",
        "category": "jewellery",
        "offer_text": "20% off on diamond collections",
        "price_range": "₹40,000–₹2,00,000",
        "valid_till": "2025-07-05",
        "source": "in-store promo"
    },
    {
        "store_name": "Ranka Jewellers",
        "city": "Pune",
        "category": "jewellery",
        "offer_text": "Free gold coin on ₹75K+ purchases",
        "price_range": "₹75,000+",
        "valid_till": "2025-07-15",
        "source": "Facebook ad"
    }
]

for offer in jewellery_offers:
    res = supabase.table("offers").insert(offer).execute()
    print(res)