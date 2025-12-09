"""
Exact matching system for identifying identical products across stores.
Uses canonical key generation to group exact matches.
"""
from typing import List, Dict, Set
from collections import defaultdict
import time
from preprocessing import extract_product_attributes


class ExactMatcher:
    """
    Exact matching system using canonical keys.
    Groups identical products across different stores.
    """
    
    def __init__(self):
        """Initialize the exact matcher."""
        self.match_groups = {}  # canonical_key -> list of products
        self.product_to_key = {}  # productID -> canonical_key
        self.products = {}  # productID -> product dict
        
        print("Initialized ExactMatcher")
    
    def create_canonical_key(self, product_name: str) -> str:
        """
        Create canonical key from product name.
        Format: {brand}_{product_type}_{size}_{unit}
        
        Args:
            product_name: Product name string
            
        Returns:
            Canonical key string
        """
        attrs = extract_product_attributes(product_name)
        
        brand = attrs['brand'] or 'unknown'
        product_type = attrs['product_type'] or 'unknown'
        size = attrs['size']
        unit = attrs['unit']
        
        # Handle products without size
        if size is None or unit is None:
            # Use product type only (for products without size info)
            key = f"{brand}_{product_type}_nosize"
        else:
            # Convert size to string, handle floats
            size_str = str(int(size)) if size == int(size) else str(size)
            key = f"{brand}_{product_type}_{size_str}_{unit}"
        
        # Clean the key (remove extra spaces, special chars)
        key = key.replace(' ', '_').replace('__', '_').lower()
        
        return key
    
    def build_exact_matches(self, products: List[Dict]) -> None:
        """
        Build exact match groups from list of products.
        
        Args:
            products: List of product dictionaries
        """
        print(f"\nBuilding exact match groups for {len(products)} products...")
        start_time = time.time()
        
        for i, product in enumerate(products):
            product_id = product['productID']
            product_name = product['productName']
            
            # Create canonical key
            canonical_key = self.create_canonical_key(product_name)
            
            # Store product
            self.products[product_id] = product
            self.product_to_key[product_id] = canonical_key
            
            # Add to match group
            if canonical_key not in self.match_groups:
                self.match_groups[canonical_key] = []
            self.match_groups[canonical_key].append(product)
            
            # Progress indicator
            if (i + 1) % 1000 == 0:
                print(f"  Processed {i + 1}/{len(products)} products...")
        
        elapsed_time = time.time() - start_time
        print(f"  Exact match groups built in {elapsed_time:.2f} seconds")
        print(f"  Total unique products: {len(self.match_groups)}")
        print(f"  Average: {elapsed_time/len(products)*1000:.2f} ms per product")
    
    def get_exact_matches(self, product_id: str) -> List[Dict]:
        """
        Get all exact matches for a given product.
        
        Args:
            product_id: Product ID to query
            
        Returns:
            List of matching products (excluding self)
        """
        if product_id not in self.product_to_key:
            return []
        
        canonical_key = self.product_to_key[product_id]
        matches = self.match_groups.get(canonical_key, [])
        
        # Remove self from matches
        matches = [p for p in matches if p['productID'] != product_id]
        
        return matches
    
    def get_match_group(self, product_id: str) -> List[Dict]:
        """
        Get the entire match group for a product (including self).
        
        Args:
            product_id: Product ID to query
            
        Returns:
            List of all products in the match group
        """
        if product_id not in self.product_to_key:
            return []
        
        canonical_key = self.product_to_key[product_id]
        return self.match_groups.get(canonical_key, [])
    
    def get_match_statistics(self) -> Dict:
        """
        Get statistics about exact matching.
        
        Returns:
            Dictionary with statistics
        """
        total_products = len(self.products)
        total_groups = len(self.match_groups)
        
        # Count products with matches (group size > 1)
        products_with_matches = 0
        group_sizes = []
        
        for group in self.match_groups.values():
            group_size = len(group)
            group_sizes.append(group_size)
            if group_size > 1:
                products_with_matches += group_size
        
        # Calculate coverage
        coverage = (products_with_matches / total_products * 100) if total_products > 0 else 0
        
        # Average group size (for groups with matches)
        groups_with_matches = [size for size in group_sizes if size > 1]
        avg_group_size = sum(groups_with_matches) / len(groups_with_matches) if groups_with_matches else 0
        
        return {
            'total_products': total_products,
            'total_unique_products': total_groups,
            'products_with_matches': products_with_matches,
            'coverage_percentage': coverage,
            'avg_products_per_group': avg_group_size,
            'largest_group_size': max(group_sizes) if group_sizes else 0
        }
    
    def get_sample_groups(self, num_samples: int = 5, min_group_size: int = 2) -> List[List[Dict]]:
        """
        Get sample match groups for inspection.
        
        Args:
            num_samples: Number of sample groups to return
            min_group_size: Minimum group size to include
            
        Returns:
            List of match groups
        """
        sample_groups = []
        
        for group in self.match_groups.values():
            if len(group) >= min_group_size:
                sample_groups.append(group)
                if len(sample_groups) >= num_samples:
                    break
        
        return sample_groups


if __name__ == "__main__":
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
            'productName': 'National Banana Jelly 80g',
            'availableAt': 'Al-Fatah',
            'originalPrice': 168
        },
        {
            'productID': '4',
            'productName': 'National Strawberry Jelly 80gm',
            'availableAt': 'Raja Sahib',
            'originalPrice': 175
        },
        {
            'productID': '5',
            'productName': 'Nestle KitKat 500ml',
            'availableAt': 'Jalal Sons',
            'originalPrice': 200
        }
    ]
    
    # Create matcher
    matcher = ExactMatcher()
    
    # Build matches
    matcher.build_exact_matches(sample_products)
    
    # Get matches for product 1
    print("\nExact matches for 'National Banana Jelly 80gm' (Rahim Store):")
    matches = matcher.get_exact_matches('1')
    for match in matches:
        print(f"  - {match['productName']} at {match['availableAt']} - Rs.{match['originalPrice']}")
    
    # Get statistics
    print("\nExact Matching Statistics:")
    stats = matcher.get_match_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
