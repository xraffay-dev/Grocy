# Grocy - Online Grocery Store Frontend

A modern, responsive frontend for an online grocery store built with React, TypeScript, and Tailwind CSS.

## Features

- 🛒 **Shopping Experience**
  - Browse products by category
  - Product search and filtering
  - Detailed product pages
  - Shopping cart with quantity management
  - Checkout process

- 👤 **User Management**
  - User registration and login
  - User account dashboard
  - Order history tracking

- 📱 **Responsive Design**
  - Mobile-first approach
  - Fully responsive across all devices
  - Modern UI with smooth animations

- 🎨 **Modern UI/UX**
  - Clean and intuitive interface
  - Fast navigation
  - Accessible components

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Icon library

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/       # Reusable UI components
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── Layout.tsx
│   └── ProductCard.tsx
├── contexts/         # React context providers
│   ├── AuthContext.tsx
│   └── CartContext.tsx
├── pages/           # Page components
│   ├── Home.tsx
│   ├── Products.tsx
│   ├── ProductDetail.tsx
│   ├── Cart.tsx
│   ├── Checkout.tsx
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Account.tsx
│   ├── OrderHistory.tsx
│   ├── Contact.tsx
│   └── About.tsx
├── data/            # Mock data
│   └── mockProducts.ts
├── App.tsx          # Main app component with routing
├── main.tsx         # Entry point
└── index.css        # Global styles
```

## Pages

- **Home** (`/`) - Landing page with featured products and categories
- **Products** (`/products`) - Browse all products with filters
- **Product Detail** (`/product/:id`) - Individual product page
- **Cart** (`/cart`) - Shopping cart
- **Checkout** (`/checkout`) - Checkout process
- **Login** (`/login`) - User login
- **Register** (`/register`) - User registration
- **Account** (`/account`) - User account dashboard
- **Order History** (`/orders`) - Past orders
- **Contact** (`/contact`) - Contact form
- **About** (`/about`) - About page

## Features in Detail

### Shopping Cart
- Add/remove items
- Update quantities
- Persistent cart state (using React Context)
- Real-time price calculations

### Product Filtering
- Filter by category
- Price range filtering
- Sort by name or price

### Authentication
- Mock authentication system
- User session management
- Protected routes

## Development

The project uses Vite for fast development with HMR (Hot Module Replacement). All components are written in TypeScript for type safety.

## License

This project is for demonstration purposes.

