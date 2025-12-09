"""
FILE 1: mongodb_extract.py
===========================
Extracts all products from MongoDB and saves to CSV

Run: python mongodb_extract.py
Output: all_products.csv
Time: ~2 minutes
"""

from pymongo import MongoClient
import pandas as pd
from datetime import datetime

class ProductExtractor:
    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="Grocy"):
        """
        Initialize MongoDB connection
        
        Args:
            mongo_uri: MongoDB connection string
            db_name: Database name
        """
        print("Connecting to MongoDB...")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        
        # Your 5 collections
        self.collections = ['Al-Fatah', 'Jalal Sons', 'Metro', 'Rahim Store', 'Raja Sahib']
        
        print(f"Connected to database: {db_name}")
        print(f"Collections: {', '.join(self.collections)}")
    
    def extract_all_products(self):
        """
        Extract all products from all 5 stores
        
        Returns:
            DataFrame with all products
        """
        print("\n" + "="*70)
        print("EXTRACTING PRODUCTS FROM MONGODB")
        print("="*70 + "\n")
        
        all_products = []
        
        for collection_name in self.collections:
            print(f"Processing {collection_name}...")
            
            try:
                collection = self.db[collection_name]
                
                # Count documents
                count = collection.count_documents({})
                print(f"Found {count} products")
                
                # Extract all documents
                products = collection.find({})
                
                for product in products:
                    # Extract relevant fields
                    all_products.append({
                        '_id': str(product['_id']),
                        'name': product.get('productName', '').strip(),
                        'price': float(product.get('discountedPrice', product.get('originalPrice', 0))),
                        'original_price': float(product.get('originalPrice', 0)),
                        'discount': float(product.get('discount', 0)),
                        'store': product.get('availableAt', collection_name),
                        'url': product.get('productURL', ''),
                        'image': product.get('productImage', ''),
                        'description': product.get('productDescription', ''),
                        'product_id': product.get('productID', '')
                    })
                
                print(f"Extracted {len([p for p in all_products if p['store'] == collection_name])} products")
                
            except Exception as e:
                print(f"Error extracting from {collection_name}: {e}")
                continue
        
        # Convert to DataFrame
        df = pd.DataFrame(all_products)
        
        # Data cleaning
        print("\nCleaning data...")
        
        # Remove products with empty names
        original_len = len(df)
        df = df[df['name'].str.len() > 0]
        df = df[df['name'].notna()]
        print(f"Removed {original_len - len(df)} products with empty names")
        
        # Remove exact duplicates within same store
        original_len = len(df)
        print("Duplicates:", df.duplicated(subset=['name', 'store'], keep='first').sum())
        df = df.drop_duplicates(subset=['name', 'store'], keep='first')
        print(f"Removed {original_len - len(df)} exact duplicates")
        
        # Reset index
        df = df.reset_index(drop=True)
        
        # Summary
        print("\n" + "="*70)
        print("EXTRACTION COMPLETE")
        print("="*70)
        print(f"Total products: {len(df)}")
        print(f"\nDistribution by store:")
        print(df['store'].value_counts().to_string())
        
        print(f"\nPrice statistics:")
        print(f"  Min: Rs. {df['price'].min():.2f}")
        print(f"  Max: Rs. {df['price'].max():.2f}")
        print(f"  Average: Rs. {df['price'].mean():.2f}")
        print(f"  Median: Rs. {df['price'].median():.2f}")
        
        return df
    
    def save_to_csv(self, df, filename='all_products.csv'):
        """
        Save products to CSV file
        
        Args:
            df: Products DataFrame
            filename: Output filename
        """
        df.to_csv(filename, index=False)
        print(f"\nSaved {len(df)} products to '{filename}'")
        
        # Show sample
        print("\nSample products:")
        print(df[['name', 'store', 'price']].head(10).to_string())
        
        return filename
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()
        print("\nMongoDB connection closed")


def main():
    """
    Main execution function
    """
    print("="*70)
    print("PRODUCT EXTRACTION FROM MONGODB")
    print("="*70)
    
    # Configuration
    MONGO_URI = "mongodb://localhost:27017/"  # Update if needed
    DB_NAME = "Grocy"
    OUTPUT_FILE = "all_products.csv"
    
    try:
        # Initialize extractor
        extractor = ProductExtractor(mongo_uri=MONGO_URI, db_name=DB_NAME)
        
        # Extract products
        products_df = extractor.extract_all_products()
        
        # Save to CSV
        extractor.save_to_csv(products_df, OUTPUT_FILE)
        
        # Close connection
        extractor.close()
        
        print("\nSUCCESS! You can now proceed to Step 2: train_model_v5.py")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("Please check your MongoDB connection and database name")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())