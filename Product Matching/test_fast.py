"""
Product Matching System - Fast Test Tool (Uses MongoDB)
========================================================
Fast testing tool that queries pre-generated matches from MongoDB.

Run save_matches_to_db.py ONCE, then use this for instant testing!
"""

from pymongo import MongoClient
from preprocessing import extract_product_attributes


class FastProductMatchTester:
    """
    Fast tester that queries MongoDB instead of rebuilding matcher.
    """
    
    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="Grocy"):
        """Connect to MongoDB."""
        print("\n" + "=" * 80)
        print(" Fast Product Match Tester (MongoDB)")
        print("=" * 80)
        print("\n Connecting to MongoDB...")
        
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.matches_collection = self.db["Product Matches"]
        count = self.matches_collection.count_documents({})
        print(f" Loaded {count:,} products from database")
        print("\n Status: READY!\n")
    
    def search_products(self, query):
        """Search products by name."""
        results = self.matches_collection.find(
            {"product_name": {"$regex": query, "$options": "i"}},
            limit=20
        )
        return list(results)
    
    def get_product_by_id(self, product_id):
        """Get product by ID."""
        return self.matches_collection.find_one({"product_id": product_id})
    
    def display_matches(self, product_data):
        """Display matches for a product."""
        if not product_data:
            print("\n No data found for this product")
            return
        
        print("\n" + "=" * 80)
        print(" QUERY PRODUCT")
        print("=" * 80)
        print(f" Name: {product_data['product_name']}")
        print(f" Store: {product_data['store']}")
        print(f" Price: Rs. {product_data['price']:.2f}")
        
        if product_data.get('brand'):
            print(f" Brand: {product_data['brand']}")
        if product_data.get('size'):
            print(f" Size: {product_data['size']}{product_data.get('unit', '')}")
        if product_data.get('price_per_unit'):
            print(f" Price per unit: Rs. {product_data['price_per_unit']:.2f} {product_data.get('unit_label', '')}")
        
        exact_matches = product_data.get('exact_matches', [])
        semantic_matches = product_data.get('semantic_matches', [])
        
        print("\n" + "=" * 80)
        print(f" MATCHES: {len(exact_matches)} Exact + {len(semantic_matches)} Semantic")
        print("=" * 80)
        
        if exact_matches:
            print("\n EXACT MATCHES (Same product, same size):")
            for i, match in enumerate(exact_matches[:5], 1):
                print(f"\n  {i}. {match['name']}")
                print(f"     Store: {match['store']}")
                print(f"     Price: Rs. {match['price']:.2f}")
                if match.get('price_per_unit'):
                    print(f"     Price per unit: Rs. {match['price_per_unit']:.2f} {match.get('unit_label', '')}")
                if match['savings'] > 0:
                    print(f"     SAVE Rs. {match['savings']:.2f} ({match['savings_percent']:.1f}%)")
        
        if semantic_matches:
            print("\n SEMANTIC MATCHES (Same product, different sizes):")
            for i, match in enumerate(semantic_matches[:5], 1):
                print(f"\n  {i}. {match['name']}")
                print(f"     Store: {match['store']}")
                print(f"     Size: {match.get('size', 'N/A')}{match.get('unit', '')}")
                print(f"     Price: Rs. {match['price']:.2f}")
                if match.get('price_per_unit'):
                    print(f"     Price per unit: Rs. {match['price_per_unit']:.2f} {match.get('unit_label', '')}")
        
        best_deal = product_data.get('best_deal')
        if best_deal:
            print("\n" + "=" * 80)
            print(" BEST DEAL")
            print("=" * 80)
            print(f" {best_deal['name']}")
            print(f" Store: {best_deal['store']}")
            print(f" Size: {best_deal.get('size', 'N/A')}{best_deal.get('unit', '')}")
            print(f" Price: Rs. {best_deal['price']:.2f}")
            if best_deal.get('price_per_unit'):
                print(f" Price per unit: Rs. {best_deal['price_per_unit']:.2f} {best_deal.get('unit_label', '')}")
        
        savings = product_data.get('savings_analysis')
        if savings:
            print(f"\n Savings: Rs. {savings['savings_per_unit']:.2f} per unit ({savings['savings_percentage']:.1f}%)")
    
    def interactive_search(self):
        """Interactive search interface."""
        print("\n" + "=" * 80)
        print(" INTERACTIVE PRODUCT MATCHER")
        print("=" * 80)
        print("\n Commands:")
        print("   search <query> - Search for products")
        print("   match <number> - Get matches for product #")
        print("   stats - Show database statistics")
        print("   quit - Exit")
        print("=" * 80 + "\n")
        
        search_results = None
        
        while True:
            command = input("\n Enter command: ").strip().lower()
            
            if command == 'quit' or command == 'q':
                print("\n Goodbye!")
                break
            
            elif command == 'stats':
                self.show_statistics()
            
            elif command.startswith('search '):
                query = command[7:]
                search_results = self.search_products(query)
                
                if len(search_results) == 0:
                    print(f"\n No products found for '{query}'")
                else:
                    print(f"\n Found {len(search_results)} products:\n")
                    
                    for i, product in enumerate(search_results, 1):
                        print(f" {i}. {product['product_name']}")
                        print(f"    Store: {product['store']} | Price: Rs. {product['price']:.2f}")
                        print(f"    Matches: {product['total_exact_matches']} exact + {product['total_semantic_matches']} semantic")
            
            elif command.startswith('match '):
                try:
                    num = int(command[6:])
                    
                    if search_results is None or len(search_results) == 0:
                        print("\n Please search for products first")
                        continue
                    
                    if num < 1 or num > len(search_results):
                        print(f"\n Invalid number. Choose 1-{len(search_results)}")
                        continue
                    
                    product = search_results[num - 1]
                    self.display_matches(product)
                    
                except ValueError:
                    print("\n Invalid command. Use: match <number>")
            
            else:
                print("\n Unknown command. Use 'search <query>', 'match <number>', 'stats', or 'quit'")
    
    def show_statistics(self):
        """Show database statistics."""
        print("\n" + "=" * 80)
        print(" DATABASE STATISTICS")
        print("=" * 80)
        
        total = self.matches_collection.count_documents({})
        
        if total == 0:
            print("\n ⚠️  No products found in database!")
            print(" Please run 'python save_matches_to_db.py' first to generate matches.")
            return
        
        with_exact = self.matches_collection.count_documents({"total_exact_matches": {"$gt": 0}})
        with_semantic = self.matches_collection.count_documents({"total_semantic_matches": {"$gt": 0}})
        with_any = self.matches_collection.count_documents({"total_matches": {"$gt": 0}})
        with_deals = self.matches_collection.count_documents({"best_deal": {"$ne": None}})
        
        print(f"\n Total products: {total:,}")
        print(f" Products with exact matches: {with_exact:,} ({with_exact/total*100:.1f}%)")
        print(f" Products with semantic matches: {with_semantic:,} ({with_semantic/total*100:.1f}%)")
        print(f" Products with any matches: {with_any:,} ({with_any/total*100:.1f}%)")
        print(f" Products with best deals: {with_deals:,} ({with_deals/total*100:.1f}%)")
        
        pipeline = [
            {"$group": {
                "_id": None,
                "avg_exact": {"$avg": "$total_exact_matches"},
                "avg_semantic": {"$avg": "$total_semantic_matches"},
                "avg_total": {"$avg": "$total_matches"}
            }}
        ]
        
        stats = list(self.matches_collection.aggregate(pipeline))
        if stats:
            print(f"\n Average exact matches per product: {stats[0]['avg_exact']:.2f}")
            print(f" Average semantic matches per product: {stats[0]['avg_semantic']:.2f}")
            print(f" Average total matches per product: {stats[0]['avg_total']:.2f}")
    
    def test_random_products(self, n=5):
        """Test N random products."""
        print("\n" + "=" * 80)
        print(f" TESTING {n} RANDOM PRODUCTS")
        print("=" * 80)
        
        pipeline = [{"$sample": {"size": n}}]
        random_products = list(self.matches_collection.aggregate(pipeline))
        
        for i, product in enumerate(random_products, 1):
            print(f"\n{'=' * 80}")
            print(f" RANDOM PRODUCT {i}/{n}")
            print('=' * 80)
            
            self.display_matches(product)
            
            if i < n:
                input("\n Press ENTER for next product...")
    
    def cleanup(self):
        """Cleanup resources."""
        self.client.close()


def main():
    """Main testing interface."""
    print("=" * 80)
    print(" FAST PRODUCT MATCH TESTER")
    print(" Queries pre-generated matches from MongoDB")
    print("=" * 80)
    
    try:
        tester = FastProductMatchTester()
        
        while True:
            print("\n" + "=" * 80)
            print(" TESTING MENU")
            print("=" * 80)
            print(" 1. Interactive search and matching")
            print(" 2. Test specific product by name")
            print(" 3. Test N random products")
            print(" 4. Show database statistics")
            print(" 5. Exit")
            
            choice = input("\n Your choice (1-5): ").strip()
            
            if choice == '1':
                tester.interactive_search()
            
            elif choice == '2':
                query = input(" Enter product name to search: ").strip()
                results = tester.search_products(query)
                
                if len(results) == 0:
                    print(f"\n No products found for '{query}'")
                else:
                    print(f"\n Found {len(results)} products")
                    tester.display_matches(results[0])
            
            elif choice == '3':
                n = input(" How many random products to test? (default 5): ").strip()
                n = int(n) if n else 5
                tester.test_random_products(n)
            
            elif choice == '4':
                tester.show_statistics()
            
            elif choice == '5':
                print("\n Goodbye!")
                tester.cleanup()
                break
            
            else:
                print(" Invalid choice")
        
        return 0
        
    except Exception as e:
        print(f"\n ERROR: {e}")
        print("\n Make sure you've run 'python save_matches_to_db.py' first!")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
