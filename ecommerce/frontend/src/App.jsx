import React, { useState } from 'react';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [users, setUsers] = useState([
    { id: 1, username: 'john', email: 'john@example.com' },
    { id: 2, username: 'jane', email: 'jane@example.com' },
    { id: 3, username: 'alice', email: 'alice@example.com' }
  ]);
  const [newUser, setNewUser] = useState({ username: '', email: '', password: '' });

  const createUser = async () => {
    if (!newUser.username || !newUser.email || !newUser.password) {
      alert('Please fill all fields');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/graphql/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: `mutation { createUser(username: "${newUser.username}", email: "${newUser.email}", password: "${newUser.password}") { success message user { id username email } } }`
        }),
      });

      const result = await response.json();

      if (result.data?.createUser?.success) {
        alert('✅ ' + result.data.createUser.message);
        setUsers([...users, {
          id: result.data.createUser.user.id,
          username: result.data.createUser.user.username,
          email: result.data.createUser.user.email
        }]);
        setNewUser({ username: '', email: '', password: '' });
      } else {
        alert('❌ Failed to create user');
      }
    } catch (error) {
      alert('❌ Error: ' + error.message);
    }
  };

  const createOrder = async () => {
    try {
      const response = await fetch('http://localhost:8000/graphql/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: `mutation { createOrder(userId: 1) { success message order { id status } } }`
        }),
      });

      const result = await response.json();

      if (result.data?.createOrder?.success) {
        alert('✅ ' + result.data.createOrder.message);
      } else {
        alert('❌ Failed to create order');
      }
    } catch (error) {
      alert('❌ Error: ' + error.message);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <h1>🛍️ ShopFlow E-Commerce</h1>
          <nav>
            <button
              className={currentPage === 'home' ? 'active' : ''}
              onClick={() => setCurrentPage('home')}
            >
              🏠 Home
            </button>
            <button
              className={currentPage === 'users' ? 'active' : ''}
              onClick={() => setCurrentPage('users')}
            >
              👥 Users
            </button>
            <button
              className={currentPage === 'products' ? 'active' : ''}
              onClick={() => setCurrentPage('products')}
            >
              📦 Products
            </button>
            <button
              className={currentPage === 'orders' ? 'active' : ''}
              onClick={() => setCurrentPage('orders')}
            >
              🛒 Orders
            </button>
          </nav>
        </div>
      </header>

      <main className="container">
        {currentPage === 'home' && (
          <div className="page">
            <h2>🚀 Welcome to ShopFlow</h2>
            <p>A modern microservices-based e-commerce platform</p>

            <div className="stats-grid">
              <div className="stat-card">
                <h3>👥 Users</h3>
                <div className="stat-number">{users.length}</div>
              </div>
              <div className="stat-card">
                <h3>📦 Products</h3>
                <div className="stat-number">25</div>
              </div>
              <div className="stat-card">
                <h3>🛒 Orders</h3>
                <div className="stat-number">12</div>
              </div>
              <div className="stat-card">
                <h3>💰 Revenue</h3>
                <div className="stat-number">$2,450</div>
              </div>
            </div>

            <div className="quick-actions">
              <h3>Quick Actions</h3>
              <button className="action-btn" onClick={createOrder}>
                🛒 Create Test Order
              </button>
              <button className="action-btn" onClick={() => setCurrentPage('users')}>
                👥 Manage Users
              </button>
            </div>
          </div>
        )}

        {currentPage === 'users' && (
          <div className="page">
            <h2>👥 User Management</h2>

            <div className="create-user-form">
              <h3>Create New User</h3>
              <div className="form-group">
                <input
                  type="text"
                  placeholder="Username"
                  value={newUser.username}
                  onChange={(e) => setNewUser({...newUser, username: e.target.value})}
                />
                <input
                  type="email"
                  placeholder="Email"
                  value={newUser.email}
                  onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={newUser.password}
                  onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                />
                <button onClick={createUser} className="create-btn">
                  ✅ Create User
                </button>
              </div>
            </div>

            <div className="users-grid">
              {users.map(user => (
                <div key={user.id} className="user-card">
                  <div className="user-avatar">👤</div>
                  <h4>{user.username}</h4>
                  <p>{user.email}</p>
                  <small>ID: {user.id}</small>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentPage === 'products' && (
          <div className="page">
            <h2>📦 Product Catalog</h2>
            <div className="products-grid">
              {[
                { id: 1, name: 'Wireless Headphones', price: '$99.99', image: '🎧' },
                { id: 2, name: 'Smart Watch', price: '$299.99', image: '⌚' },
                { id: 3, name: 'Coffee Maker', price: '$149.99', image: '☕' },
                { id: 4, name: 'Running Shoes', price: '$129.99', image: '👟' },
                { id: 5, name: 'Laptop Backpack', price: '$79.99', image: '🎒' },
                { id: 6, name: 'Bluetooth Speaker', price: '$59.99', image: '🔊' },
              ].map(product => (
                <div key={product.id} className="product-card">
                  <div className="product-image">{product.image}</div>
                  <h4>{product.name}</h4>
                  <p className="price">{product.price}</p>
                  <button className="add-to-cart">🛒 Add to Cart</button>
                </div>
              ))}
            </div>
          </div>
        )}

        {currentPage === 'orders' && (
          <div className="page">
            <h2>🛒 Order Management</h2>
            <button onClick={createOrder} className="create-order-btn">
              ➕ Create Test Order
            </button>

            <div className="orders-list">
              {[
                { id: 1, customer: 'John Doe', status: 'PENDING', total: '$199.98' },
                { id: 2, customer: 'Jane Smith', status: 'COMPLETED', total: '$149.99' },
                { id: 3, customer: 'Alice Johnson', status: 'SHIPPED', total: '$209.98' },
              ].map(order => (
                <div key={order.id} className="order-card">
                  <div className="order-header">
                    <h4>Order #{order.id}</h4>
                    <span className={`status ${order.status.toLowerCase()}`}>
                      {order.status}
                    </span>
                  </div>
                  <p>Customer: {order.customer}</p>
                  <p className="total">Total: {order.total}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
