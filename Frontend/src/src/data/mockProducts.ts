export interface StorePrice {
  storeId: string;
  storeName: string;
  storeLogo?: string;
  price: number;
  inStock: boolean;
  link?: string;
}

export interface PromotionalBanner {
  text: string;
  type: 'price-drop' | 'save' | 'sale' | 'new';
  storeName?: string;
  amount?: number;
}

export interface Product {
  id: string;
  name: string;
  price: number; // Lowest price or default price
  image: string;
  category: string;
  description: string;
  inStock: boolean;
  rating?: number;
  reviews?: number;
  storePrices?: StorePrice[]; // Price comparison across stores
  totalReviews?: number; // Total reviews across all stores
  promotionalBanners?: PromotionalBanner[]; // Banners to show over product image
}

export interface Store {
  id: string;
  name: string;
  path: string;
  logo: string;
}

export const stores: Store[] = [
  { id: '1', name: 'Al-Fatah', path: '/stores/al-fatah', logo: '/src/data/al-fatah-logo-1.jpg' },
  { id: '2', name: 'Jalal Sons', path: '/stores/jalal-sons', logo: '/src/data/jalal-sons-logo1.jpg' },
  { id: '3', name: 'Rahim Store', path: '/stores/rahim-store', logo: '/src/data/rahim-store-logo-1.jpg' },
  { id: '4', name: 'Metro', path: '/stores/metro', logo: '/src/data/metro-logo-1.png' },
  { id: '5', name: 'Raja Sahib', path: '/stores/raja-sahib', logo: '/src/data/raja-sahib-logo-1.jpg' },
];

export const getStoreLogo = (storeName: string): string | null => {
  const store = stores.find(s => s.name === storeName);
  return store ? store.logo : null;
};

export const products: Product[] = [
  // Fruits & Vegetables
  {
    id: '1',
    name: 'Fresh Organic Apples',
    price: 3.99, // Lowest price
    image: 'https://images.unsplash.com/photo-1619546813926-78ca9b6f2b3e?w=400',
    category: 'fruits-vegetables',
    description: 'Crisp and juicy organic apples, perfect for snacking or baking.',
    inStock: true,
    rating: 4.5,
    reviews: 120,
    totalReviews: 245,
    promotionalBanners: [
      { text: 'Price drop in FreshMart', type: 'price-drop', storeName: 'FreshMart' },
      { text: 'Save $2.00', type: 'save', amount: 2.00 },
    ],
    storePrices: [
      { storeId: '1', storeName: 'FreshMart', price: 3.99, inStock: true },
      { storeId: '2', storeName: 'SuperStore', price: 4.49, inStock: true },
      { storeId: '3', storeName: 'Grocery Plus', price: 4.99, inStock: true },
      { storeId: '4', storeName: 'Value Market', price: 5.29, inStock: true },
      { storeId: '5', storeName: 'Premium Foods', price: 5.99, inStock: true },
    ],
  },
  {
    id: '2',
    name: 'Organic Bananas',
    price: 2.49, // Lowest price
    image: 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400',
    category: 'fruits-vegetables',
    description: 'Sweet and creamy organic bananas, rich in potassium.',
    inStock: true,
    rating: 4.7,
    reviews: 95,
    totalReviews: 180,
    storePrices: [
      { storeId: '1', storeName: 'FreshMart', price: 2.49, inStock: true },
      { storeId: '2', storeName: 'SuperStore', price: 2.99, inStock: true },
      { storeId: '3', storeName: 'Grocery Plus', price: 3.29, inStock: true },
      { storeId: '4', storeName: 'Value Market', price: 3.49, inStock: true },
    ],
  },
  {
    id: '3',
    name: 'Fresh Spinach',
    price: 3.49,
    image: 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400',
    category: 'fruits-vegetables',
    description: 'Fresh leafy spinach, packed with nutrients.',
    inStock: true,
    rating: 4.3,
    reviews: 78,
  },
  {
    id: '4',
    name: 'Organic Carrots',
    price: 2.49,
    image: 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400',
    category: 'fruits-vegetables',
    description: 'Crunchy organic carrots, great for salads and cooking.',
    inStock: true,
    rating: 4.6,
    reviews: 110,
  },

  // Dairy & Eggs
  {
    id: '5',
    name: 'Organic Whole Milk',
    price: 4.99, // Lowest price
    image: 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400',
    category: 'dairy-eggs',
    description: 'Fresh organic whole milk from local farms.',
    inStock: true,
    rating: 4.8,
    reviews: 200,
    totalReviews: 420,
    promotionalBanners: [
      { text: 'Save $2.50', type: 'save', amount: 2.50 },
    ],
    storePrices: [
      { storeId: '1', storeName: 'FreshMart', price: 4.99, inStock: true },
      { storeId: '2', storeName: 'SuperStore', price: 5.49, inStock: true },
      { storeId: '3', storeName: 'Grocery Plus', price: 5.99, inStock: true },
      { storeId: '4', storeName: 'Value Market', price: 6.29, inStock: true },
      { storeId: '5', storeName: 'Premium Foods', price: 6.99, inStock: true },
      { storeId: '6', storeName: 'Local Market', price: 7.49, inStock: true },
    ],
  },
  {
    id: '6',
    name: 'Free Range Eggs (12 pack)',
    price: 5.99, // Lowest price
    image: 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400',
    category: 'dairy-eggs',
    description: 'Premium free-range eggs from happy hens.',
    inStock: true,
    rating: 4.9,
    reviews: 350,
    totalReviews: 680,
    promotionalBanners: [
      { text: 'Save $2.00', type: 'save', amount: 2.00 },
    ],
    storePrices: [
      { storeId: '1', storeName: 'FreshMart', price: 5.99, inStock: true },
      { storeId: '2', storeName: 'SuperStore', price: 6.49, inStock: true },
      { storeId: '3', storeName: 'Grocery Plus', price: 6.99, inStock: true },
      { storeId: '4', storeName: 'Value Market', price: 7.29, inStock: true },
      { storeId: '5', storeName: 'Premium Foods', price: 7.99, inStock: true },
    ],
  },
  {
    id: '7',
    name: 'Greek Yogurt',
    price: 4.49,
    image: 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400',
    category: 'dairy-eggs',
    description: 'Creamy Greek yogurt, high in protein.',
    inStock: true,
    rating: 4.7,
    reviews: 180,
  },
  {
    id: '8',
    name: 'Organic Butter',
    price: 6.49,
    image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400',
    category: 'dairy-eggs',
    description: 'Rich and creamy organic butter.',
    inStock: true,
    rating: 4.6,
    reviews: 145,
  },

  // Meat & Fish
  {
    id: '9',
    name: 'Grass-Fed Beef Steak',
    price: 18.99,
    image: 'https://images.unsplash.com/photo-1603048297172-c92544798d5a?w=400',
    category: 'meat-fish',
    description: 'Premium grass-fed beef steak, tender and flavorful.',
    inStock: true,
    rating: 4.9,
    reviews: 95,
  },
  {
    id: '10',
    name: 'Fresh Salmon Fillet',
    price: 16.99,
    image: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400',
    category: 'meat-fish',
    description: 'Fresh Atlantic salmon fillet, rich in omega-3.',
    inStock: true,
    rating: 4.8,
    reviews: 120,
  },
  {
    id: '11',
    name: 'Organic Chicken Breast',
    price: 12.99,
    image: 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400',
    category: 'meat-fish',
    description: 'Tender organic chicken breast, antibiotic-free.',
    inStock: true,
    rating: 4.7,
    reviews: 200,
  },

  // Bakery
  {
    id: '12',
    name: 'Artisan Sourdough Bread',
    price: 5.99,
    image: 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400',
    category: 'bakery',
    description: 'Freshly baked artisan sourdough bread.',
    inStock: true,
    rating: 4.8,
    reviews: 165,
  },
  {
    id: '13',
    name: 'Chocolate Chip Cookies',
    price: 3.99, // Lowest price
    image: 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400',
    category: 'bakery',
    description: 'Homemade chocolate chip cookies, soft and chewy.',
    inStock: true,
    rating: 4.9,
    reviews: 280,
    totalReviews: 520,
    promotionalBanners: [
      { text: 'Price drop in FreshMart', type: 'price-drop', storeName: 'FreshMart' },
      { text: 'Save $3.00', type: 'save', amount: 3.00 },
    ],
    storePrices: [
      { storeId: '1', storeName: 'FreshMart', price: 3.99, inStock: true },
      { storeId: '2', storeName: 'SuperStore', price: 4.49, inStock: true },
      { storeId: '3', storeName: 'Grocery Plus', price: 4.99, inStock: true },
      { storeId: '4', storeName: 'Value Market', price: 5.29, inStock: true },
      { storeId: '5', storeName: 'Premium Foods', price: 5.99, inStock: true },
      { storeId: '6', storeName: 'Local Market', price: 6.49, inStock: true },
      { storeId: '7', storeName: 'Bakery Direct', price: 6.99, inStock: true },
    ],
  },
  {
    id: '14',
    name: 'Fresh Croissants (4 pack)',
    price: 6.99,
    image: 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400',
    category: 'bakery',
    description: 'Buttery French croissants, baked fresh daily.',
    inStock: true,
    rating: 4.7,
    reviews: 195,
  },

  // Beverages
  {
    id: '15',
    name: 'Fresh Orange Juice',
    price: 4.99,
    image: 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400',
    category: 'beverages',
    description: '100% pure fresh squeezed orange juice.',
    inStock: true,
    rating: 4.6,
    reviews: 150,
  },
  {
    id: '16',
    name: 'Organic Coffee Beans',
    price: 12.99,
    image: 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400',
    category: 'beverages',
    description: 'Premium organic coffee beans, medium roast.',
    inStock: true,
    rating: 4.8,
    reviews: 220,
  },
  {
    id: '17',
    name: 'Sparkling Water (12 pack)',
    price: 8.99,
    image: 'https://images.unsplash.com/photo-1523362628745-0c100150b504?w=400',
    category: 'beverages',
    description: 'Refreshing sparkling water, zero calories.',
    inStock: true,
    rating: 4.5,
    reviews: 90,
  },

  // Snacks
  {
    id: '18',
    name: 'Organic Trail Mix',
    price: 7.99,
    image: 'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=400',
    category: 'snacks',
    description: 'Healthy mix of nuts, dried fruits, and seeds.',
    inStock: true,
    rating: 4.7,
    reviews: 175,
  },
  {
    id: '19',
    name: 'Dark Chocolate Bar',
    price: 3.99, // Lowest price
    image: 'https://images.unsplash.com/photo-1606312619070-d48b4bcc2b7a?w=400',
    category: 'snacks',
    description: 'Premium 70% dark chocolate, organic and fair trade.',
    inStock: true,
    rating: 4.9,
    reviews: 300,
    totalReviews: 580,
    storePrices: [
      { storeId: '1', storeName: 'FreshMart', price: 3.99, inStock: true },
      { storeId: '2', storeName: 'SuperStore', price: 4.49, inStock: true },
      { storeId: '3', storeName: 'Grocery Plus', price: 4.99, inStock: true },
      { storeId: '4', storeName: 'Value Market', price: 5.29, inStock: true },
    ],
  },
  {
    id: '20',
    name: 'Organic Popcorn',
    price: 3.99,
    image: 'https://images.unsplash.com/photo-1586816001966-79b736744398?w=400',
    category: 'snacks',
    description: 'Light and airy organic popcorn, perfect for snacking.',
    inStock: true,
    rating: 4.4,
    reviews: 125,
  },
];

export const getProductById = (id: string): Product | undefined => {
  return products.find(p => p.id === id);
};
