import React, { useState } from 'react';
import { useMutation } from '@apollo/client';
import { CREATE_ORDER } from '../apollo/queries';
import Card from '../components/UI/Card';
import Button from '../components/UI/Button';
import { toast } from 'react-toastify';
import {
  ShoppingCartIcon,
  PlusIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  TruckIcon,
} from '@heroicons/react/24/outline';

const Orders = () => {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [createOrder, { loading: creating }] = useMutation(CREATE_ORDER);

  // Mock orders data - replace with GraphQL query
  const orders = [
    {
      id: 1,
      userId: 1,
      status: 'PENDING',
      createdAt: '2024-01-15T10:30:00Z',
      items: [
        { product_id: 1, quantity: 2, price: 99.99, name: 'Wireless Headphones' },
        { product_id: 2, quantity: 1, price: 299.99, name: 'Smart Watch' },
      ],
      total: 499.97,
      customer: { name: 'John Doe', email: 'john@example.com' },
    },
    {
      id: 2,
      userId: 2,
      status: 'COMPLETED',
      createdAt: '2024-01-14T15:45:00Z',
      items: [
        { product_id: 3, quantity: 1, price: 149.99, name: 'Coffee Maker' },
      ],
      total: 149.99,
      customer: { name: 'Jane Smith', email: 'jane@example.com' },
    },
    {
      id: 3,
      userId: 3,
      status: 'SHIPPED',
      createdAt: '2024-01-13T09:15:00Z',
      items: [
        { product_id: 4, quantity: 1, price: 129.99, name: 'Running Shoes' },
        { product_id: 5, quantity: 1, price: 79.99, name: 'Laptop Backpack' },
      ],
      total: 209.98,
      customer: { name: 'Alice Johnson', email: 'alice@example.com' },
    },
  ];

  const handleCreateOrder = async () => {
    try {
      const result = await createOrder({
        variables: {
          userId: 1,
          items: ['{"product_id": 1, "quantity": 2, "price": 29.99}'],
        },
      });

      if (result.data?.createOrder?.success) {
        toast.success(result.data.createOrder.message);
        setShowCreateForm(false);
      } else {
        toast.error('Failed to create order');
      }
    } catch (err) {
      toast.error('Error creating order: ' + err.message);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'PENDING':
        return <ClockIcon className="w-5 h-5 text-yellow-500" />;
      case 'COMPLETED':
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'SHIPPED':
        return <TruckIcon className="w-5 h-5 text-blue-500" />;
      case 'CANCELLED':
        return <XCircleIcon className="w-5 h-5 text-red-500" />;
      default:
        return <ClockIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800';
      case 'COMPLETED':
        return 'bg-green-100 text-green-800';
      case 'SHIPPED':
        return 'bg-blue-100 text-blue-800';
      case 'CANCELLED':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Order Management</h1>
          <p className="text-gray-600 mt-2">Track and manage customer orders</p>
        </div>
        <Button
          onClick={handleCreateOrder}
          loading={creating}
          className="animate-bounce-in"
        >
          <PlusIcon className="w-5 h-5 mr-2" />
          Create Test Order
        </Button>
      </div>

      {/* Order Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Total Orders', value: orders.length, color: 'blue' },
          { label: 'Pending', value: orders.filter(o => o.status === 'PENDING').length, color: 'yellow' },
          { label: 'Completed', value: orders.filter(o => o.status === 'COMPLETED').length, color: 'green' },
          { label: 'Revenue', value: `$${orders.reduce((sum, o) => sum + o.total, 0).toFixed(2)}`, color: 'purple' },
        ].map((stat, index) => (
          <Card key={stat.label} className="p-6 animate-slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
            <div className="flex items-center space-x-4">
              <div className={`p-3 bg-${stat.color}-500 rounded-lg`}>
                <ShoppingCartIcon className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                <p className="text-sm text-gray-600">{stat.label}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Orders List */}
      <div className="space-y-6">
        {orders.map((order, index) => (
          <Card 
            key={order.id} 
            className="p-6 animate-slide-up" 
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
              {/* Order Info */}
              <div className="flex-1">
                <div className="flex items-center space-x-4 mb-3">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Order #{order.id}
                  </h3>
                  <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}>
                    {getStatusIcon(order.status)}
                    <span>{order.status}</span>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
                  <div>
                    <p><span className="font-medium">Customer:</span> {order.customer.name}</p>
                    <p><span className="font-medium">Email:</span> {order.customer.email}</p>
                  </div>
                  <div>
                    <p><span className="font-medium">Date:</span> {new Date(order.createdAt).toLocaleDateString()}</p>
                    <p><span className="font-medium">Total:</span> <span className="text-green-600 font-semibold">${order.total}</span></p>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex space-x-2">
                <Button size="sm" variant="secondary">
                  View Details
                </Button>
                <Button size="sm">
                  Update Status
                </Button>
              </div>
            </div>

            {/* Order Items */}
            <div className="mt-4 pt-4 border-t border-gray-200">
              <h4 className="text-sm font-medium text-gray-900 mb-2">Items:</h4>
              <div className="space-y-2">
                {order.items.map((item, itemIndex) => (
                  <div key={itemIndex} className="flex justify-between items-center text-sm">
                    <span className="text-gray-600">
                      {item.name} × {item.quantity}
                    </span>
                    <span className="font-medium">${(item.price * item.quantity).toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {orders.length === 0 && (
        <Card className="p-12 text-center">
          <ShoppingCartIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No orders found</h3>
          <p className="text-gray-600 mb-6">Orders will appear here once customers start purchasing</p>
          <Button onClick={handleCreateOrder} loading={creating}>
            <PlusIcon className="w-5 h-5 mr-2" />
            Create Test Order
          </Button>
        </Card>
      )}
    </div>
  );
};

export default Orders;
