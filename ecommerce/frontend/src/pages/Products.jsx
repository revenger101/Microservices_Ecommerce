import React, { useState } from 'react';
import Card from '../components/UI/Card';
import Button from '../components/UI/Button';
import {
  CubeIcon,
  PlusIcon,
  MagnifyingGlassIcon,
  TagIcon,
  CurrencyDollarIcon,
} from '@heroicons/react/24/outline';

const Products = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Mock product data - replace with GraphQL query
  const products = [
    {
      id: 1,
      name: 'Wireless Headphones',
      price: 99.99,
      category: 'Electronics',
      stock: 25,
      image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop',
      description: 'High-quality wireless headphones with noise cancellation',
    },
    {
      id: 2,
      name: 'Smart Watch',
      price: 299.99,
      category: 'Electronics',
      stock: 15,
      image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop',
      description: 'Advanced smartwatch with health monitoring features',
    },
    {
      id: 3,
      name: 'Coffee Maker',
      price: 149.99,
      category: 'Home & Kitchen',
      stock: 8,
      image: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=300&fit=crop',
      description: 'Premium coffee maker for the perfect brew',
    },
    {
      id: 4,
      name: 'Running Shoes',
      price: 129.99,
      category: 'Sports',
      stock: 30,
      image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop',
      description: 'Comfortable running shoes for all terrains',
    },
    {
      id: 5,
      name: 'Laptop Backpack',
      price: 79.99,
      category: 'Accessories',
      stock: 12,
      image: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop',
      description: 'Durable laptop backpack with multiple compartments',
    },
    {
      id: 6,
      name: 'Bluetooth Speaker',
      price: 59.99,
      category: 'Electronics',
      stock: 20,
      image: 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=300&h=300&fit=crop',
      description: 'Portable Bluetooth speaker with excellent sound quality',
    },
  ];

  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const categories = [...new Set(products.map(p => p.category))];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Product Catalog</h1>
          <p className="text-gray-600 mt-2">Manage your product inventory</p>
        </div>
        <Button className="animate-bounce-in">
          <PlusIcon className="w-5 h-5 mr-2" />
          Add Product
        </Button>
      </div>

      {/* Search and Filters */}
      <Card className="p-6">
        <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
          <div className="flex-1 relative">
            <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search products..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <select className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option value="">All Categories</option>
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>
      </Card>

      {/* Products Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProducts.map((product, index) => (
          <Card 
            key={product.id} 
            className="overflow-hidden animate-slide-up" 
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="aspect-w-16 aspect-h-9">
              <img
                src={product.image}
                alt={product.name}
                className="w-full h-48 object-cover"
              />
            </div>
            
            <div className="p-6">
              <div className="flex items-start justify-between mb-2">
                <h3 className="text-lg font-semibold text-gray-900 line-clamp-1">
                  {product.name}
                </h3>
                <span className={`px-2 py-1 text-xs rounded-full ${
                  product.stock > 10 
                    ? 'bg-green-100 text-green-800' 
                    : product.stock > 0 
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  {product.stock} in stock
                </span>
              </div>
              
              <div className="flex items-center space-x-2 mb-3">
                <TagIcon className="w-4 h-4 text-gray-400" />
                <span className="text-sm text-gray-600">{product.category}</span>
              </div>
              
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                {product.description}
              </p>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-1">
                  <CurrencyDollarIcon className="w-5 h-5 text-green-600" />
                  <span className="text-xl font-bold text-gray-900">
                    {product.price}
                  </span>
                </div>
                
                <div className="flex space-x-2">
                  <Button size="sm" variant="secondary">
                    Edit
                  </Button>
                  <Button size="sm">
                    View
                  </Button>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {filteredProducts.length === 0 && (
        <Card className="p-12 text-center">
          <CubeIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No products found</h3>
          <p className="text-gray-600 mb-6">
            {searchTerm ? 'Try adjusting your search terms' : 'Get started by adding your first product'}
          </p>
          <Button>
            <PlusIcon className="w-5 h-5 mr-2" />
            Add Product
          </Button>
        </Card>
      )}

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="p-6 text-center">
          <div className="text-2xl font-bold text-gray-900">{products.length}</div>
          <div className="text-sm text-gray-600">Total Products</div>
        </Card>
        <Card className="p-6 text-center">
          <div className="text-2xl font-bold text-gray-900">{categories.length}</div>
          <div className="text-sm text-gray-600">Categories</div>
        </Card>
        <Card className="p-6 text-center">
          <div className="text-2xl font-bold text-gray-900">
            {products.reduce((sum, p) => sum + p.stock, 0)}
          </div>
          <div className="text-sm text-gray-600">Total Stock</div>
        </Card>
        <Card className="p-6 text-center">
          <div className="text-2xl font-bold text-green-600">
            ${products.reduce((sum, p) => sum + (p.price * p.stock), 0).toFixed(2)}
          </div>
          <div className="text-sm text-gray-600">Inventory Value</div>
        </Card>
      </div>
    </div>
  );
};

export default Products;
