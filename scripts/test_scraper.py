import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../backend/.env')

async def test_setup():
    """Test if everything is set up correctly"""
    print("TESTING SCRAPER SETUP")
    print("=" * 30)
    
    # Check SERPAPI_KEY
    api_key = os.getenv("SERPAPI_KEY")
    if api_key and api_key != "your_serpapi_key_here":
        print("SERPAPI_KEY: FOUND")
    else:
        print("SERPAPI_KEY: NOT SET")
        print("Please add your SerpAPI key to backend/.env file")
        print("Get key from: https://serpapi.com/")
        return False
    
    # Check required packages
    try:
        import aiohttp
        print("aiohttp: INSTALLED")
    except ImportError:
        print("aiohttp: MISSING - run: pip install aiohttp")
        return False
    
    try:
        import pandas
        print("pandas: INSTALLED")
    except ImportError:
        print("pandas: MISSING - run: pip install pandas")
        return False
    
    # Check directories
    data_dir = '../data'
    if os.path.exists(data_dir):
        print("data directory: EXISTS")
    else:
        print("data directory: CREATED")
        os.makedirs(data_dir, exist_ok=True)
    
    # Test SerpAPI connection
    print("\nTesting SerpAPI connection...")
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            params = {
                "engine": "google",
                "q": "test",
                "api_key": api_key
            }
            async with session.get("https://serpapi.com/search", params=params) as response:
                if response.status == 200:
                    print("SerpAPI connection: SUCCESS")
                    return True
                else:
                    print(f"SerpAPI connection: FAILED - Status {response.status}")
                    return False
    except Exception as e:
        print(f"SerpAPI connection: ERROR - {e}")
        return False

async def main():
    success = await test_setup()
    
    if success:
        print("\nALL TESTS PASSED")
        print("Ready to run: python serpapi_scraper.py")
    else:
        print("\nSETUP INCOMPLETE")
        print("Fix the issues above before running the scraper")

if __name__ == "__main__":
    asyncio.run(main()) 