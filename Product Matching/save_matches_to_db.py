"""
Save product matches to MongoDB using the 4-stage matching system.

This script generates product matches for all products in the database
and saves them to a MongoDB collection for efficient retrieval.
"""

import sys
sys.path.insert(0, 'venv/Lib/site-packages')

import numpy as np
from pymongo import MongoClient
from datetime import datetime
from tqdm import tqdm
from data_loader import ProductDataLoader
from product_matcher import ProductMatcher
from price_comparator import PriceComparator
from preprocessing import extract_product_attributes


class ProductMatchSaver:
    """
    Handles generation and storage of product matches using the 4-stage system.
    """
    
    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="Grocy"):
        """Initialize MongoDB connection and load the matching system."""
        print("Connecting to MongoDB...")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        
        print("Loading Product Matching System...")
        print("  Stage 1: LSH Blocking")
        print("  Stage 2: Exact Matching")
        print("  Stage 3: Semantic Matching")
        print("  Stage 4: Price Comparison")
        
        self.loader = ProductDataLoader()
        self.products = self.loader.load_products_from_stores()
        
        print(f"\nLoaded {len(self.products):,} products")
        
        print("\nBuilding matcher indices...")
        self.matcher = ProductMatcher()
        self.matcher.build_index(self.products)
        
        print(f"System: READY!\n")
    
    def generate_matches_for_all(self, top_k=10):
        """Generate matches for all products."""
        print("\n" + "=" * 80)
        print("GENERATING PRODUCT MATCHES FOR ALL PRODUCTS")
        print("=" * 80 + "\n")
        
        print(f"Configuration:")
        print(f"  Products: {len(self.products):,}")
        print(f"  Matches per product: {top_k}")
        print(f"  Match types: Exact + Semantic")
        
        documents = []
        comparator = PriceComparator()
        
        for product in tqdm(self.products, desc="Generating matches"):
            product_id = product['productID']
            
            price_data = self.matcher.get_price_comparison(product_id)
            
            if not price_data:
                continue
            
            query_product = price_data['query_product']
            matches = price_data['matches'][:top_k]
            price_comparison = price_data['price_comparison']
            savings = price_data['savings_analysis']
            
            query_attrs = extract_product_attributes(query_product['productName'])
            query_price_info = comparator.calculate_price_per_unit(query_product)
            
            exact_matches = []
            semantic_matches = []
            
            for match in matches:
                match_product = match['product']
                match_type = match['match_type']
                confidence = match['confidence']
                
                match_attrs = extract_product_attributes(match_product['productName'])
                match_price_info = comparator.calculate_price_per_unit(match_product)
                
                savings_amount = query_product['originalPrice'] - match_product['originalPrice']
                savings_pct = (savings_amount / query_product['originalPrice'] * 100) if query_product['originalPrice'] > 0 else 0
                
                match_doc = {
                    'product_id': match_product['productID'],
                    'name': match_product['productName'],
                    'store': match_product['availableAt'],
                    'price': float(match_product['originalPrice']),
                    'discounted_price': float(match_product.get('discountedPrice', 0)),
                    'discount': float(match_product.get('discount', 0)),
                    'url': match_product.get('productURL', ''),
                    'image': match_product.get('productImage', ''),
                    'brand': match_attrs['brand'],
                    'size': float(match_attrs['size']) if match_attrs['size'] else None,
                    'unit': match_attrs['unit'],
                    'match_type': match_type,
                    'confidence': float(confidence),
                    'savings': float(savings_amount),
                    'savings_percent': float(savings_pct),
                    'price_per_unit': float(match_price_info['price_per_unit']) if match_price_info['price_per_unit'] else None,
                    'unit_label': match_price_info['unit_label']
                }
                
                if match_type == 'exact':
                    exact_matches.append(match_doc)
                else:
                    semantic_matches.append(match_doc)
            
            best_deal = None
            if price_comparison and len(price_comparison) > 1:
                best_price_comparison = price_comparison[0]
                best_product = best_price_comparison['product']
                best_price_info = best_price_comparison['price_info']
                
                if best_product['productID'] != product_id:
                    best_attrs = extract_product_attributes(best_product['productName'])
                    best_deal = {
                        'product_id': best_product['productID'],
                        'name': best_product['productName'],
                        'store': best_product['availableAt'],
                        'price': float(best_product['originalPrice']),
                        'price_per_unit': float(best_price_info['price_per_unit']) if best_price_info['price_per_unit'] else None,
                        'unit_label': best_price_info['unit_label'],
                        'size': float(best_attrs['size']) if best_attrs['size'] else None,
                        'unit': best_attrs['unit'],
                        'url': best_product.get('productURL', ''),
                        'image': best_product.get('productImage', '')
                    }
            
            savings_analysis = None
            if savings['has_savings']:
                savings_analysis = {
                    'savings_per_unit': float(savings['savings_per_unit']),
                    'savings_percentage': float(savings['savings_percentage'])
                }
            
            document = {
                'product_id': product_id,
                'product_name': query_product['productName'],
                'store': query_product['availableAt'],
                'price': float(query_product['originalPrice']),
                'discounted_price': float(query_product.get('discountedPrice', 0)),
                'discount': float(query_product.get('discount', 0)),
                'url': query_product.get('productURL', ''),
                'image': query_product.get('productImage', ''),
                'brand': query_attrs['brand'],
                'size': float(query_attrs['size']) if query_attrs['size'] else None,
                'unit': query_attrs['unit'],
                'price_per_unit': float(query_price_info['price_per_unit']) if query_price_info['price_per_unit'] else None,
                'unit_label': query_price_info['unit_label'],
                'exact_matches': exact_matches,
                'semantic_matches': semantic_matches,
                'best_deal': best_deal,
                'savings_analysis': savings_analysis,
                'total_exact_matches': len(exact_matches),
                'total_semantic_matches': len(semantic_matches),
                'total_matches': len(exact_matches) + len(semantic_matches),
                'model_version': 'v1_4stage',
                'created_at': datetime.now(),
                'last_updated': datetime.now()
            }
            
            documents.append(document)
        
        print(f"\nGenerated matches for {len(documents):,} products")
        
        total_exact = sum(doc['total_exact_matches'] for doc in documents)
        total_semantic = sum(doc['total_semantic_matches'] for doc in documents)
        total_matches = sum(doc['total_matches'] for doc in documents)
        avg_matches = total_matches / len(documents) if documents else 0
        
        print(f"\nStatistics:")
        print(f"  Total exact matches: {total_exact:,}")
        print(f"  Total semantic matches: {total_semantic:,}")
        print(f"  Total matches: {total_matches:,}")
        print(f"  Average per product: {avg_matches:.1f}")
        print(f"  Products with matches: {sum(1 for d in documents if d['total_matches'] > 0):,}")
        print(f"  Products with best deals: {sum(1 for d in documents if d['best_deal'] is not None):,}")
        
        return documents
    
    def save_to_mongodb(self, documents, collection_name='Product Matches'):
        """Save match documents to MongoDB."""
        print("\n" + "=" * 80)
        print(f"SAVING TO MONGODB: {collection_name}")
        print("=" * 80 + "\n")
        
        if collection_name in self.db.list_collection_names():
            print(f"Collection '{collection_name}' already exists")
            response = input("  Overwrite? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled")
                return
            
            self.db[collection_name].drop()
            print(f"Dropped existing collection")
        
        collection = self.db[collection_name]
        
        print(f"Inserting {len(documents):,} documents...")
        batch_size = 1000
        
        for i in tqdm(range(0, len(documents), batch_size), desc="Inserting batches"):
            batch = documents[i:i+batch_size]
            collection.insert_many(batch)
        
        print(f"\nSaved {len(documents):,} documents to MongoDB")
        
        print("\nCreating indexes...")
        collection.create_index('product_id')
        collection.create_index('product_name')
        collection.create_index('store')
        collection.create_index('brand')
        collection.create_index([('price_per_unit', 1)])
        print("Indexes created")
    
    def cleanup(self):
        """Cleanup resources."""
        self.loader.close()


def main():
    """Main execution function."""
    print("=" * 80)
    print("SAVE PRODUCT MATCHES TO MONGODB")
    print("4-Stage Matching System | Cross-Store Price Comparison")
    print("=" * 80)
    
    try:
        MONGO_URI = "mongodb://localhost:27017/"
        DB_NAME = "Grocy"
        COLLECTION_NAME = "Product Matches"
        TOP_K = 10
        
        saver = ProductMatchSaver(mongo_uri=MONGO_URI, db_name=DB_NAME)
        
        documents = saver.generate_matches_for_all(top_k=TOP_K)
        
        saver.save_to_mongodb(documents, COLLECTION_NAME)
        
        print("\n" + "=" * 80)
        print("ALL DONE!")
        print("=" * 80)
        print(f"\nMongoDB Collection: {COLLECTION_NAME}")
        print(f"Total documents: {len(documents):,}")
        print("\nProduct matching system is ready to use!")
        
        saver.cleanup()
        
        return 0
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
