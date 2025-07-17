import pandas as pd
import os

def view_csv():
    """View the scraped jewelry stores CSV - clean professional output"""
    csv_file = '../data/kolhapur_jewelry_stores.csv'
    
    if not os.path.exists(csv_file):
        print("ERROR: CSV file not found")
        print("Run the scraper first: python serpapi_scraper.py")
        return
    
    try:
        df = pd.read_csv(csv_file)
        
        print("KOLHAPUR JEWELRY STORES - CSV VIEWER")
        print("=" * 50)
        print(f"File: {csv_file}")
        print(f"Total stores: {len(df)}")
        
        print(f"\nDATA COMPLETENESS:")
        for col in df.columns:
            filled = df[col].notna().sum()
            empty_count = len(df) - filled
            percentage = (filled / len(df)) * 100
            print(f"  {col}: {filled}/{len(df)} filled ({percentage:.1f}%) - {empty_count} empty")
        
        print(f"\nALL STORES:")
        print(df.to_string(index=False, max_colwidth=40))
        
        # Show stores with ratings
        rated = df[df['rating'].notna() & (df['rating'] != '')]
        if len(rated) > 0:
            print(f"\nSTORES WITH RATINGS:")
            rated_sorted = rated.sort_values('rating', ascending=False)
            print(rated_sorted[['title', 'rating', 'phone']].to_string(index=False))
        
        # Show stores with websites
        with_websites = df[df['website'].notna() & (df['website'] != '')]
        if len(with_websites) > 0:
            print(f"\nSTORES WITH WEBSITES:")
            print(with_websites[['title', 'website']].to_string(index=False, max_colwidth=50))
        
        # Show stores with phone numbers
        with_phones = df[df['phone'].notna() & (df['phone'] != '')]
        if len(with_phones) > 0:
            print(f"\nSTORES WITH PHONE NUMBERS:")
            print(with_phones[['title', 'phone']].to_string(index=False))
        
    except Exception as e:
        print(f"ERROR reading CSV: {e}")

if __name__ == "__main__":
    view_csv() 