import React from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/UI/Card';
import Button from '../components/UI/Button';
import {
  ShoppingCartIcon,
  UserGroupIcon,
  CubeIcon,
  ChartBarIcon,
  SparklesIcon,
  RocketLaunchIcon,
} from '@heroicons/react/24/outline';

const Home = () => {
  const features = [
    {
      icon: UserGroupIcon,
      title: 'User Management',
      description: 'Create and manage users with our GraphQL API',
      link: '/users',
      color: 'from-blue-500 to-cyan-500',
    },
    {
      icon: CubeIcon,
      title: 'Product Catalog',
      description: 'Browse and manage your product inventory',
      link: '/products',
      color: 'from-purple-500 to-pink-500',
    },
    {
      icon: ShoppingCartIcon,
      title: 'Order Processing',
      description: 'Handle orders with our microservices architecture',
      link: '/orders',
      color: 'from-green-500 to-emerald-500',
    },
    {
      icon: ChartBarIcon,
      title: 'Analytics',
      description: 'Track performance and sales metrics',
      link: '/analytics',
      color: 'from-orange-500 to-red-500',
    },
  ];

  const stats = [
    { label: 'Active Users', value: '1,234', icon: UserGroupIcon },
    { label: 'Products', value: '567', icon: CubeIcon },
    { label: 'Orders Today', value: '89', icon: ShoppingCartIcon },
    { label: 'Revenue', value: '$12,345', icon: ChartBarIcon },
  ];

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-6">
        <div className="flex justify-center">
          <div className="p-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full">
            <RocketLaunchIcon className="w-12 h-12 text-white" />
          </div>
        </div>
        <h1 className="text-4xl md:text-6xl font-bold gradient-text">
          Welcome to ShopFlow
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          A modern, microservices-based e-commerce platform built with React, Django, and GraphQL.
          Experience the future of online shopping management.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button size="lg" className="animate-bounce-in">
            <SparklesIcon className="w-5 h-5 mr-2" />
            Get Started
          </Button>
          <Button variant="secondary" size="lg">
            View Documentation
          </Button>
        </div>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.label} className="p-6 animate-slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  <p className="text-sm text-gray-600">{stat.label}</p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Features Section */}
      <div className="space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Platform Features</h2>
          <p className="text-lg text-gray-600">
            Explore the powerful features of our e-commerce platform
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card 
                key={feature.title} 
                className="p-8 animate-slide-up" 
                style={{ animationDelay: `${index * 0.2}s` }}
              >
                <div className="space-y-4">
                  <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-lg flex items-center justify-center`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900">{feature.title}</h3>
                  <p className="text-gray-600">{feature.description}</p>
                  <Link to={feature.link}>
                    <Button variant="secondary" size="sm">
                      Explore →
                    </Button>
                  </Link>
                </div>
              </Card>
            );
          })}
        </div>
      </div>

      {/* CTA Section */}
      <Card className="p-8 text-center bg-gradient-to-r from-blue-500 to-purple-600 text-white">
        <h2 className="text-2xl font-bold mb-4">Ready to start building?</h2>
        <p className="text-blue-100 mb-6">
          Join thousands of developers using our platform to build amazing e-commerce experiences.
        </p>
        <Button variant="secondary" size="lg">
          Start Your Journey
        </Button>
      </Card>
    </div>
  );
};

export default Home;
