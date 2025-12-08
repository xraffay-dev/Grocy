"""
Unified product matching system integrating all three stages.
Combines LSH blocking, exact matching, and semantic matching.
"""
from typing import List, Dict
from data_loader import ProductDataLoader
from blocking import ProductBlocker
from exact_matcher import ExactMatcher
from semantic_matcher import SemanticMatcher
from preprocessing import extract_product_attributes


class ProductMatcher:
    """
    Unified product matching system combining all stages.
    """
    
    def __init__(self):
        """Initialize all matchers."""
        print("Initializing Product Matcher...")
        
        self.blocker = None
        self.exact_matcher = None
        self.semantic_matcher = None
        self.products = {}
    
    def build_index(self, products: List[Dict]) -> None:
        """
        Build indices for all matching stages.
        
        Args:
            products: List of product dictionaries
        """
        print(f"\nBuilding indices for {len(products)} products...")
        
        self.products = {p['productID']: p for p in products}
        
        print("\n[Stage 1] Building LSH Blocker...")
        self.blocker = ProductBlocker()
        self.blocker.build_index(products)
        
        print("\n[Stage 2] Building Exact Matcher...")
        self.exact_matcher = ExactMatcher()
        self.exact_matcher.build_exact_matches(products)
        
        print("\n[Stage 3] Building Semantic Matcher...")
        self.semantic_matcher = SemanticMatcher()
        self.semantic_matcher.build_faiss_index(products)
        
        print("\nAll indices built successfully!")
    
    def find_all_matches(self, product_id: str) -> Dict:
        """
        Find all matches for a product using all stages.
        
        Args:
            product_id: Product ID to query
            
        Returns:
            Dictionary with exact and semantic matches
        """
        if product_id not in self.products:
            return {'exact_matches': [], 'semantic_matches': []}
        
        exact_matches = self.exact_matcher.get_exact_matches(product_id)
        
        semantic_matches = self.semantic_matcher.get_semantic_matches(
            product_id, k=20, min_similarity=0.85
        )
        
        exact_ids = {m['productID'] for m in exact_matches}
        semantic_matches = [
            m for m in semantic_matches 
            if m['product']['productID'] not in exact_ids
        ]
        
        return {
            'exact_matches': exact_matches,
            'semantic_matches': semantic_matches
        }
    
    def get_match_results(self, product_id: str) -> List[Dict]:
        """
        Get structured match results with confidence levels.
        
        Args:
            product_id: Product ID to query
            
        Returns:
            List of match dictionaries sorted by confidence
        """
        matches = self.find_all_matches(product_id)
        
        results = []
        
        for match in matches['exact_matches']:
            results.append({
                'product': match,
                'match_type': 'exact',
                'confidence': 1.0,
                'similarity': 1.0
            })
        
        for match in matches['semantic_matches']:
            results.append({
                'product': match['product'],
                'match_type': 'semantic',
                'confidence': match['confidence'],
                'similarity': match['similarity']
            })
        
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return results
    
    def get_statistics(self) -> Dict:
        """
        Get overall matching statistics.
        
        Returns:
            Dictionary with statistics from all stages
        """
        exact_stats = self.exact_matcher.get_match_statistics()
        semantic_stats = self.semantic_matcher.get_statistics()
        blocking_stats = self.blocker.get_statistics()
        
        return {
            'total_products': exact_stats['total_products'],
            'exact_match_coverage': exact_stats['coverage_percentage'],
            'semantic_match_coverage': semantic_stats['estimated_coverage'],
            'avg_exact_matches': exact_stats['avg_products_per_group'],
            'avg_semantic_matches': semantic_stats['avg_matches_per_product'],
            'blocking_reduction': blocking_stats['reduction_ratio']
        }
    
    def get_price_comparison(self, product_id: str) -> Dict:
        """
        Get matches with price comparison analysis.
        
        Args:
            product_id: Product ID to query
            
        Returns:
            Dictionary with matches and price analysis
        """
        from price_comparator import PriceComparator
        
        if product_id not in self.products:
            return None
        
        product = self.products[product_id]
        results = self.get_match_results(product_id)
        
        all_products = [product] + [r['product'] for r in results]
        
        comparator = PriceComparator()
        comparison = comparator.compare_products(all_products)
        ranked = comparator.rank_by_value(comparison)
        savings = comparator.get_savings_analysis(ranked)
        
        return {
            'query_product': product,
            'matches': results,
            'price_comparison': ranked,
            'savings_analysis': savings
        }


if __name__ == "__main__":
    from data_loader import ProductDataLoader
    
    print("Loading products...")
    loader = ProductDataLoader()
    products = loader.load_products_from_stores()
    print(f"Loaded {len(products)} products")
    
    matcher = ProductMatcher()
    matcher.build_index(products)
    
    print("\nTesting on first product:")
    product = products[0]
    print(f"Product: {product['productName']}")
    
    results = matcher.get_match_results(product['productID'])
    
    print(f"\nFound {len(results)} total matches:")
    for i, result in enumerate(results[:5], 1):
        print(f"{i}. {result['product']['productName']}")
        print(f"   Type: {result['match_type']}, Confidence: {result['confidence']:.3f}")
    
    stats = matcher.get_statistics()
    print("\nOverall Statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    loader.close()
