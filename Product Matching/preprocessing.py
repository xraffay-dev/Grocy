"""
Text preprocessing utilities for product name matching.
"""
import re
from typing import List, Set
import config


def clean_product_name(product_name: str) -> str:
    """
    Clean and normalize product name.
    
    Args:
        product_name: Raw product name string
        
    Returns:
        Cleaned product name (lowercase, no special chars, normalized whitespace)
    """
    if not product_name:
        return ""
    
    # Convert to lowercase
    cleaned = product_name.lower()
    
    # Remove special characters but keep alphanumeric and spaces
    cleaned = re.sub(r'[^a-z0-9\s]', ' ', cleaned)
    
    # Normalize whitespace (replace multiple spaces with single space)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Strip leading/trailing whitespace
    cleaned = cleaned.strip()
    
    return cleaned


def generate_ngrams(text: str, n: int = None) -> Set[str]:
    """
    Generate character-level n-grams from text.
    
    Args:
        text: Input text string
        n: N-gram size (default: from config)
        
    Returns:
        Set of n-gram strings
    """
    if n is None:
        n = config.N_GRAM_SIZE
    
    if not text or len(text) < n:
        return {text} if text else set()
    
    ngrams = set()
    for i in range(len(text) - n + 1):
        ngrams.add(text[i:i+n])
    
    return ngrams


def tokenize(text: str) -> List[str]:
    """
    Split text into word tokens.
    
    Args:
        text: Input text string
        
    Returns:
        List of word tokens
    """
    if not text:
        return []
    
    # Split on whitespace
    tokens = text.split()
    
    return tokens


# Common grocery brands (lowercase)
COMMON_BRANDS = {
    'national', 'nestle', 'unilever', 'cocacola', 'coca cola', 'pepsi',
    'lays', 'kurkure', 'knorr', 'lipton', 'surf', 'ariel', 'tide',
    'colgate', 'close up', 'lux', 'dove', 'pantene', 'head shoulders',
    'pampers', 'huggies', 'johnson', 'dettol', 'safeguard', 'lifebuoy',
    'shan', 'shan foods', 'national foods', 'mitchells', 'tapal',
    'brooke bond', 'lipton yellow label', 'vital', 'dalda', 'habib',
    'english biscuit', 'peek freans', 'sooper', 'bisconni', 'rio'
}

# Brand aliases (normalize variations)
BRAND_ALIASES = {
    'coca cola': 'cocacola',
    'head shoulders': 'head and shoulders',
    'head & shoulders': 'head and shoulders',
    'shan foods': 'shan',
    'national foods': 'national',
    'lipton yellow label': 'lipton',
    'brooke bond': 'brookebond',
    'peek freans': 'peekfreans',
    'english biscuit': 'englishbiscuit'
}


def normalize_unit(size: float, unit: str) -> tuple:
    """
    Normalize units to standard forms.
    Weight: grams (g), Volume: milliliters (ml)
    
    Args:
        size: Size value
        unit: Unit string
        
    Returns:
        Tuple of (normalized_size, normalized_unit)
    """
    unit = unit.lower()
    
    # Weight conversions to grams
    if unit in ['kg', 'kilogram']:
        return size * 1000, 'g'
    elif unit in ['gm', 'gram', 'grams']:
        return size, 'g'
    elif unit == 'g':
        return size, 'g'
    
    # Volume conversions to milliliters
    elif unit in ['l', 'ltr', 'litre', 'liter', 'liters', 'litres']:
        return size * 1000, 'ml'
    elif unit in ['ml', 'milliliter', 'millilitre']:
        return size, 'ml'
    
    # Keep other units as-is
    else:
        return size, unit


def extract_brand(product_name: str) -> str:
    """
    Extract brand name from product name.
    
    Args:
        product_name: Product name string
        
    Returns:
        Brand name (lowercase) or empty string if not found
    """
    cleaned = clean_product_name(product_name)
    tokens = cleaned.split()
    
    if not tokens:
        return ''
    
    # Check first 1-3 words for brand match
    for length in [3, 2, 1]:
        if len(tokens) >= length:
            potential_brand = ' '.join(tokens[:length])
            
            # Check if it's a known brand
            if potential_brand in COMMON_BRANDS:
                # Normalize using aliases
                return BRAND_ALIASES.get(potential_brand, potential_brand)
            
            # Check for partial matches
            for brand in COMMON_BRANDS:
                if potential_brand.startswith(brand) or brand.startswith(potential_brand):
                    return BRAND_ALIASES.get(brand, brand)
    
    # Default to first word as brand
    return tokens[0]


def extract_size_info(product_name: str) -> dict:
    """
    Extract size/quantity information from product name.
    
    Args:
        product_name: Product name string
        
    Returns:
        Dictionary with 'size', 'unit', and 'name_without_size'
    """
    # Pattern to match sizes: 80gm, 1.5L, 500ml, 250g, etc.
    size_pattern = r'(\d+(?:\.\d+)?)\s*(gm|g|kg|ml|l|ltr|litre|oz|pack|pcs|piece|gram|grams|kilogram|liter|liters|litre|litres)'
    
    match = re.search(size_pattern, product_name.lower())
    
    if match:
        size = float(match.group(1))
        unit = match.group(2)
        
        # Normalize unit
        normalized_size, normalized_unit = normalize_unit(size, unit)
        
        # Remove size from product name
        name_without_size = re.sub(size_pattern, '', product_name, flags=re.IGNORECASE)
        name_without_size = re.sub(r'\s+', ' ', name_without_size).strip()
        
        return {
            'size': normalized_size,
            'unit': normalized_unit,
            'name_without_size': name_without_size
        }
    
    return {
        'size': None,
        'unit': None,
        'name_without_size': product_name
    }


def extract_product_attributes(product_name: str) -> dict:
    """
    Extract comprehensive product attributes for exact matching.
    
    Args:
        product_name: Product name string
        
    Returns:
        Dictionary with brand, product_type, size, unit, and original_name
    """
    # Extract brand
    brand = extract_brand(product_name)
    
    # Extract size info
    size_info = extract_size_info(product_name)
    
    # Extract product type (name without brand and size)
    product_type = size_info['name_without_size']
    
    # Remove brand from product type
    if brand:
        # Clean product type
        cleaned_type = clean_product_name(product_type)
        cleaned_brand = clean_product_name(brand)
        
        # Remove brand from beginning
        if cleaned_type.startswith(cleaned_brand):
            cleaned_type = cleaned_type[len(cleaned_brand):].strip()
        
        product_type = cleaned_type
    else:
        product_type = clean_product_name(product_type)
    
    return {
        'brand': brand,
        'product_type': product_type,
        'size': size_info['size'],
        'unit': size_info['unit'],
        'original_name': product_name
    }


def fuzzy_brand_match(brand1: str, brand2: str, threshold: float = 0.85) -> bool:
    """
    Check if two brands match using fuzzy string matching.
    
    Args:
        brand1: First brand name
        brand2: Second brand name
        threshold: Similarity threshold (0.0 to 1.0)
        
    Returns:
        True if brands match, False otherwise
    """
    from rapidfuzz import fuzz
    
    if not brand1 or not brand2:
        return False
    
    similarity = fuzz.ratio(brand1.lower(), brand2.lower()) / 100.0
    
    return similarity >= threshold


if __name__ == "__main__":
    # Test preprocessing functions
    test_names = [
        "National Banana Jelly 80gm",
        "Coca-Cola Zero 1.5L",
        "Nestle KitKat 500ml",
        "Lays Chips 250g"
    ]
    
    print("Testing preprocessing functions:\n")
    
    for name in test_names:
        print(f"Original: {name}")
        
        cleaned = clean_product_name(name)
        print(f"Cleaned: {cleaned}")
        
        ngrams = generate_ngrams(cleaned, n=3)
        print(f"N-grams (first 10): {list(ngrams)[:10]}")
        
        tokens = tokenize(cleaned)
        print(f"Tokens: {tokens}")
        
        size_info = extract_size_info(name)
        print(f"Size info: {size_info}")
        
        print("-" * 60)
