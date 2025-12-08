"""
MinHash LSH-based blocking system for efficient product candidate generation.
"""
from datasketch import MinHash, MinHashLSH
from typing import List, Dict, Tuple, Set
import time
import config
from preprocessing import clean_product_name, generate_ngrams


class ProductBlocker:
    """
    MinHash LSH-based blocking system for product matching.
    Reduces comparison space from O(n²) to O(n) by grouping similar products.
    """
    
    def __init__(self, num_perm: int = None, threshold: float = None):
        """
        Initialize the product blocker.
        
        Args:
            num_perm: Number of permutations for MinHash (default: from config)
            threshold: Jaccard similarity threshold (default: from config)
        """
        self.num_perm = num_perm or config.LSH_NUM_PERM
        self.threshold = threshold or config.LSH_THRESHOLD
        
        # Initialize LSH index
        self.lsh = MinHashLSH(threshold=self.threshold, num_perm=self.num_perm)
        
        # Store product metadata for quick lookup
        self.products = {}  # productID -> product dict
        self.minhashes = {}  # productID -> MinHash object
        
        print(f"Initialized ProductBlocker with num_perm={self.num_perm}, threshold={self.threshold}")
    
    def create_minhash(self, product_name: str) -> MinHash:
        """
        Create MinHash signature from product name.
        
        Args:
            product_name: Product name string
            
        Returns:
            MinHash object
        """
        # Clean product name
        cleaned_name = clean_product_name(product_name)
        
        # Generate n-grams
        ngrams = generate_ngrams(cleaned_name)
        
        # Create MinHash
        minhash = MinHash(num_perm=self.num_perm)
        for ngram in ngrams:
            minhash.update(ngram.encode('utf-8'))
        
        return minhash
    
    def build_index(self, products: List[Dict]) -> None:
        """
        Build LSH index from list of products.
        
        Args:
            products: List of product dictionaries
        """
        print(f"\nBuilding LSH index for {len(products)} products...")
        start_time = time.time()
        
        for i, product in enumerate(products):
            product_id = product['productID']
            product_name = product['productName']
            
            # Create MinHash signature
            minhash = self.create_minhash(product_name)
            
            # Store product and minhash
            self.products[product_id] = product
            self.minhashes[product_id] = minhash
            
            # Insert into LSH index
            self.lsh.insert(product_id, minhash)
            
            # Progress indicator
            if (i + 1) % 1000 == 0:
                print(f"  Processed {i + 1}/{len(products)} products...")
        
        elapsed_time = time.time() - start_time
        print(f"✓ Index built in {elapsed_time:.2f} seconds")
        print(f"  Average: {elapsed_time/len(products)*1000:.2f} ms per product")
    
    def query_candidates(self, product_id: str, max_candidates: int = 200) -> List[Dict]:
        """
        Find candidate products similar to the given product.
        
        Args:
            product_id: Product ID to query
            max_candidates: Maximum number of candidates to return
            
        Returns:
            List of candidate product dictionaries
        """
        if product_id not in self.minhashes:
            return []
        
        # Query LSH index
        minhash = self.minhashes[product_id]
        candidate_ids = self.lsh.query(minhash)
        
        # Remove self from candidates
        candidate_ids = [cid for cid in candidate_ids if cid != product_id]
        
        # Limit number of candidates
        candidate_ids = candidate_ids[:max_candidates]
        
        # Return candidate products
        candidates = [self.products[cid] for cid in candidate_ids]
        
        return candidates
    
    def get_all_candidate_pairs(self, max_candidates_per_product: int = 200) -> List[Tuple[Dict, Dict]]:
        """
        Generate all candidate pairs for matching.
        
        Args:
            max_candidates_per_product: Maximum candidates per product
            
        Returns:
            List of (product1, product2) tuples
        """
        print(f"\nGenerating candidate pairs...")
        start_time = time.time()
        
        pairs = []
        seen_pairs = set()  # To avoid duplicate pairs
        
        for product_id in self.products:
            candidates = self.query_candidates(product_id, max_candidates_per_product)
            
            for candidate in candidates:
                # Create sorted pair to avoid duplicates (A,B) and (B,A)
                pair_key = tuple(sorted([product_id, candidate['productID']]))
                
                if pair_key not in seen_pairs:
                    seen_pairs.add(pair_key)
                    pairs.append((self.products[product_id], candidate))
        
        elapsed_time = time.time() - start_time
        print(f"Generated {len(pairs)} candidate pairs in {elapsed_time:.2f} seconds")
        
        return pairs
    
    def get_statistics(self) -> Dict:
        """
        Get blocking statistics.
        
        Returns:
            Dictionary with statistics
        """
        total_products = len(self.products)
        
        # Calculate average candidates per product
        total_candidates = 0
        for product_id in self.products:
            candidates = self.query_candidates(product_id)
            total_candidates += len(candidates)
        
        avg_candidates = total_candidates / total_products if total_products > 0 else 0
        
        # Calculate reduction ratio
        total_possible_pairs = (total_products * (total_products - 1)) / 2
        actual_pairs = total_candidates / 2  # Each pair counted twice
        reduction_ratio = (1 - actual_pairs / total_possible_pairs) * 100 if total_possible_pairs > 0 else 0
        
        return {
            'total_products': total_products,
            'avg_candidates_per_product': avg_candidates,
            'total_possible_pairs': int(total_possible_pairs),
            'actual_candidate_pairs': int(actual_pairs),
            'reduction_ratio': reduction_ratio
        }


if __name__ == "__main__":
    # Test the blocker with sample data
    sample_products = [
        {
            'productID': '1',
            'productName': 'National Banana Jelly 80gm',
            'availableAt': 'Rahim Store',
            'originalPrice': 170
        },
        {
            'productID': '2',
            'productName': 'National Banana Jelly 80gm',
            'availableAt': 'Metro',
            'originalPrice': 165
        },
        {
            'productID': '3',
            'productName': 'National Strawberry Jelly 80gm',
            'availableAt': 'Al-Fatah',
            'originalPrice': 175
        },
        {
            'productID': '4',
            'productName': 'Nestle KitKat 500ml',
            'availableAt': 'Raja Sahib',
            'originalPrice': 200
        }
    ]
    
    # Create blocker
    blocker = ProductBlocker()
    
    # Build index
    blocker.build_index(sample_products)
    
    # Query candidates
    print("\nQuerying candidates for 'National Banana Jelly 80gm' (Rahim Store):")
    candidates = blocker.query_candidates('1')
    for candidate in candidates:
        print(f"  - {candidate['productName']} at {candidate['availableAt']}")
    
    # Get statistics
    print("\nBlocking Statistics:")
    stats = blocker.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
