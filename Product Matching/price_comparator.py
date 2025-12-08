"""
Price comparison and ranking system for matched products.
Calculates price-per-unit, normalizes sizes, and ranks by value.
"""
from typing import List, Dict
from preprocessing import extract_product_attributes


class PriceComparator:
    """
    Price comparison system for matched products.
    """
    
    def __init__(self):
        """Initialize price comparator."""
        pass
    
    def get_effective_price(self, product: Dict) -> float:
        """
        Get the effective price (discounted if available, else original).
        
        Args:
            product: Product dictionary
            
        Returns:
            Effective price
        """
        discount = product.get('discount', 0)
        if discount > 0 and product.get('discountedPrice', 0) > 0:
            return product['discountedPrice']
        return product.get('originalPrice', 0)
    
    def normalize_to_standard_unit(self, size: float, unit: str) -> tuple:
        """
        Normalize to standard units for comparison.
        Weight: per 100g, Volume: per liter
        
        Args:
            size: Size value
            unit: Unit string
            
        Returns:
            Tuple of (standard_unit_label, multiplier)
        """
        if unit == 'g':
            return ('per 100g', 100.0)
        elif unit == 'ml':
            return ('per liter', 1000.0)
        else:
            return (f'per {unit}', 1.0)
    
    def calculate_price_per_unit(self, product: Dict) -> Dict:
        """
        Calculate price-per-unit for a product.
        
        Args:
            product: Product dictionary
            
        Returns:
            Dictionary with price analysis
        """
        attrs = extract_product_attributes(product['productName'])
        price = self.get_effective_price(product)
        
        if not attrs['size'] or not attrs['unit']:
            return {
                'price': price,
                'price_per_unit': None,
                'unit_label': None,
                'size': None,
                'unit': None
            }
        
        unit_label, standard_size = self.normalize_to_standard_unit(
            attrs['size'], attrs['unit']
        )
        
        price_per_unit = (price / attrs['size']) * standard_size
        
        return {
            'price': price,
            'price_per_unit': price_per_unit,
            'unit_label': unit_label,
            'size': attrs['size'],
            'unit': attrs['unit'],
            'has_discount': product.get('discount', 0) > 0
        }
    
    def compare_products(self, products: List[Dict]) -> List[Dict]:
        """
        Compare a list of matched products.
        
        Args:
            products: List of product dictionaries
            
        Returns:
            List of products with price analysis
        """
        results = []
        
        for product in products:
            price_info = self.calculate_price_per_unit(product)
            
            results.append({
                'product': product,
                'price_info': price_info
            })
        
        return results
    
    def rank_by_value(self, comparison_results: List[Dict]) -> List[Dict]:
        """
        Rank products by best value (lowest price-per-unit).
        
        Args:
            comparison_results: List from compare_products()
            
        Returns:
            Sorted list with best value first
        """
        valid_results = [
            r for r in comparison_results 
            if r['price_info']['price_per_unit'] is not None
        ]
        
        invalid_results = [
            r for r in comparison_results 
            if r['price_info']['price_per_unit'] is None
        ]
        
        valid_results.sort(key=lambda x: x['price_info']['price_per_unit'])
        
        return valid_results + invalid_results
    
    def get_savings_analysis(self, ranked_results: List[Dict]) -> Dict:
        """
        Calculate savings analysis.
        
        Args:
            ranked_results: Ranked list from rank_by_value()
            
        Returns:
            Dictionary with savings information
        """
        if len(ranked_results) < 2:
            return {
                'has_savings': False,
                'best_deal': None,
                'worst_deal': None,
                'savings_per_unit': 0,
                'savings_percentage': 0
            }
        
        valid_results = [
            r for r in ranked_results 
            if r['price_info']['price_per_unit'] is not None
        ]
        
        if len(valid_results) < 2:
            return {
                'has_savings': False,
                'best_deal': None,
                'worst_deal': None,
                'savings_per_unit': 0,
                'savings_percentage': 0
            }
        
        best = valid_results[0]
        worst = valid_results[-1]
        
        savings_per_unit = worst['price_info']['price_per_unit'] - best['price_info']['price_per_unit']
        savings_percentage = (savings_per_unit / worst['price_info']['price_per_unit']) * 100
        
        return {
            'has_savings': True,
            'best_deal': best,
            'worst_deal': worst,
            'savings_per_unit': savings_per_unit,
            'savings_percentage': savings_percentage
        }
    
    def format_comparison_results(self, ranked_results: List[Dict], 
                                  product_name: str = None) -> str:
        """
        Format comparison results as human-readable text.
        
        Args:
            ranked_results: Ranked list from rank_by_value()
            product_name: Optional product name for header
            
        Returns:
            Formatted string
        """
        if not ranked_results:
            return "No products to compare"
        
        lines = []
        
        if product_name:
            lines.append(f"\nPrice Comparison: {product_name}")
            lines.append("=" * 80)
        
        for i, result in enumerate(ranked_results, 1):
            product = result['product']
            price_info = result['price_info']
            
            store = product['availableAt']
            product_name = product['productName']
            
            if price_info['price_per_unit'] is not None:
                size_str = f"{price_info['size']}{price_info['unit']}"
                price_str = f"Rs. {price_info['price']:.2f}"
                per_unit_str = f"Rs. {price_info['price_per_unit']:.2f} {price_info['unit_label']}"
                
                discount_str = " (DISCOUNTED)" if price_info['has_discount'] else ""
                best_str = " - BEST VALUE" if i == 1 else ""
                
                lines.append(f"\n{i}. {product_name}")
                lines.append(f"   Store: {store}")
                lines.append(f"   Size: {size_str}, Price: {price_str}{discount_str}")
                lines.append(f"   Price per unit: {per_unit_str}{best_str}")
            else:
                lines.append(f"\n{i}. {product_name}")
                lines.append(f"   Store: {store}")
                lines.append(f"   Price: Rs. {price_info['price']:.2f}")
                lines.append(f"   (No size information available)")
        
        savings = self.get_savings_analysis(ranked_results)
        if savings['has_savings']:
            lines.append(f"\nSavings Analysis:")
            lines.append(f"  Best deal saves Rs. {savings['savings_per_unit']:.2f} {ranked_results[0]['price_info']['unit_label']}")
            lines.append(f"  Savings: {savings['savings_percentage']:.1f}% compared to most expensive")
        
        return "\n".join(lines)


if __name__ == "__main__":
    sample_products = [
        {
            'productID': '1',
            'productName': 'National Banana Jelly 80gm',
            'availableAt': 'Rahim Store',
            'originalPrice': 170,
            'discountedPrice': 0,
            'discount': 0
        },
        {
            'productID': '2',
            'productName': 'National Banana Jelly 160gm',
            'availableAt': 'Metro',
            'originalPrice': 320,
            'discountedPrice': 0,
            'discount': 0
        },
        {
            'productID': '3',
            'productName': 'National Banana Jelly 80gm',
            'availableAt': 'Al-Fatah',
            'originalPrice': 180,
            'discountedPrice': 165,
            'discount': 10
        }
    ]
    
    comparator = PriceComparator()
    
    comparison = comparator.compare_products(sample_products)
    ranked = comparator.rank_by_value(comparison)
    
    print(comparator.format_comparison_results(ranked, "National Banana Jelly"))
