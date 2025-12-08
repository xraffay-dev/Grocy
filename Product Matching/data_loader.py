"""
MongoDB data loading utilities for product matching system.
"""
from pymongo import MongoClient
from typing import List, Dict
import config


class ProductDataLoader:
    """Handles loading product data from MongoDB collections."""
    
    def __init__(self):
        """Initialize MongoDB connection."""
        self.client = MongoClient(config.MONGODB_URI)
        self.db = self.client[config.DATABASE_NAME]
    
    def load_products_from_stores(self) -> List[Dict]:
        """
        Load all products from all store collections.
        
        Returns:
            List of product dictionaries with standardized fields.
        """
        all_products = []
        
        for store_name in config.STORE_COLLECTIONS:
            collection = self.db[store_name]
            products = collection.find({})
            
            for product in products:
                # Standardize product data
                standardized_product = {
                    'productID': product.get('productID', str(product['_id'])),
                    'productName': product.get('productName', ''),
                    'availableAt': product.get('availableAt', store_name),
                    'originalPrice': product.get('originalPrice', 0),
                    'discountedPrice': product.get('discountedPrice', 0),
                    'discount': product.get('discount', 0),
                    'productURL': product.get('productURL', ''),
                    'productImage': product.get('productImage', ''),
                    'productDescription': product.get('productDescription', ''),
                    '_id': str(product['_id'])
                }
                all_products.append(standardized_product)
        
        return all_products
    
    def get_product_count(self) -> Dict[str, int]:
        """
        Get product count for each store.
        
        Returns:
            Dictionary mapping store names to product counts.
        """
        counts = {}
        
        for store_name in config.STORE_COLLECTIONS:
            collection = self.db[store_name]
            counts[store_name] = collection.count_documents({})
        
        return counts
    
    def get_total_product_count(self) -> int:
        """
        Get total product count across all stores.
        
        Returns:
            Total number of products.
        """
        counts = self.get_product_count()
        return sum(counts.values())
    
    def close(self):
        """Close MongoDB connection."""
        self.client.close()


if __name__ == "__main__":
    # Test the data loader
    loader = ProductDataLoader()
    
    print("Product counts by store:")
    counts = loader.get_product_count()
    for store, count in counts.items():
        print(f"  {store}: {count}")
    
    print(f"\nTotal products: {loader.get_total_product_count()}")
    
    # Load sample products
    print("\nLoading products...")
    products = loader.load_products_from_stores()
    print(f"Loaded {len(products)} products")
    
    # Show sample product
    if products:
        print("\nSample product:")
        sample = products[0]
        for key, value in sample.items():
            print(f"  {key}: {value}")
    
    loader.close()
