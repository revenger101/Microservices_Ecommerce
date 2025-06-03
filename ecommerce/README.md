# 🛍️ ShopFlow - Modern E-Commerce Microservices Platform

A cutting-edge, scalable e-commerce platform built with modern microservices architecture, featuring React frontend, Django GraphQL API Gateway, and Python gRPC microservices.

![Platform Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue)
![Frontend](https://img.shields.io/badge/Frontend-React-61dafb)
![Backend](https://img.shields.io/badge/Backend-Django%20%7C%20gRPC-green)
![Database](https://img.shields.io/badge/Database-PostgreSQL-336791)
![Cache](https://img.shields.io/badge/Cache-Redis-dc382d)

## 🚀 Features

- **🎨 Modern React Frontend** - Beautiful, responsive UI with Tailwind CSS
- **🔗 GraphQL API Gateway** - Unified API layer with Django and Graphene
- **⚡ gRPC Microservices** - High-performance inter-service communication
- **🗄️ Multi-Database Architecture** - Separate PostgreSQL instances per service
- **📊 Redis Caching** - Fast data access and session management
- **🔄 Async Task Processing** - Celery for background jobs
- **🐳 Docker Containerization** - Easy deployment and scaling
- **🔐 Authentication Ready** - JWT token support
- **📱 Mobile Responsive** - Works perfectly on all devices

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │  Microservices  │
│   React + CSS   │◄──►│   Django        │◄──►│   User Service  │
│   Port: 3000    │    │   GraphQL       │    │   Order Service │
│                 │    │   Port: 8000    │    │   gRPC Servers  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │     Redis       │    │   PostgreSQL    │
                       │   Caching       │    │   Databases     │
                       │   Celery        │    │   User + Order  │
                       │   Port: 6379    │    │   Port: 5432    │
                       └─────────────────┘    └─────────────────┘
```

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern UI library
- **Tailwind CSS** - Utility-first CSS framework
- **Apollo Client** - GraphQL client
- **React Router** - Client-side routing
- **React Toastify** - Notifications
- **Heroicons** - Beautiful icons

### Backend
- **Django 4.2** - Web framework
- **Graphene-Django** - GraphQL integration
- **Django REST Framework** - API development
- **Django CORS Headers** - Cross-origin requests
- **gRPC** - High-performance RPC framework
- **Protocol Buffers** - Data serialization

### Databases & Cache
- **PostgreSQL 13** - Primary databases
- **Redis 6** - Caching and message broker

### DevOps & Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Web server (production)
- **Celery** - Distributed task queue

### Development Tools
- **Python 3.9+** - Backend language
- **Node.js 18+** - Frontend tooling
- **npm** - Package management
- **Git** - Version control

## 📁 Project Structure

```
ecommerce/
├── 🎨 frontend/                 # React Frontend
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Page components
│   │   ├── apollo/            # GraphQL configuration
│   │   └── App.jsx            # Main application
│   ├── public/                # Static assets
│   ├── package.json           # Dependencies
│   └── Dockerfile             # Frontend container
│
├── 🌐 api_gateway/             # Django API Gateway
│   ├── gateway/               # Main application
│   │   ├── schema.py          # GraphQL schema
│   │   ├── services.py        # gRPC client services
│   │   └── resolvers.py       # GraphQL resolvers
│   ├── api_gateway/           # Django settings
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Gateway container
│
├── 👥 user_service/            # User Microservice
│   ├── user_service.py        # gRPC server implementation
│   ├── models.py              # Database models
│   ├── database.py            # Database connection
│   ├── requirements.txt       # Dependencies
│   └── Dockerfile             # Service container
│
├── 🛒 order_service/           # Order Microservice
│   ├── order_service.py       # gRPC server implementation
│   ├── models.py              # Database models
│   ├── database.py            # Database connection
│   ├── requirements.txt       # Dependencies
│   └── Dockerfile             # Service container
│
├── 📋 protos/                  # Protocol Buffer definitions
│   ├── user_service.proto     # User service interface
│   └── order_service.proto    # Order service interface
│
├── 🐳 docker-compose.yml       # Multi-service orchestration
├── 📖 README.md               # This file
└── 🎯 frontend-demo.html      # Standalone demo
```

## 🚀 Quick Start

### Prerequisites
- **Docker** & **Docker Compose** installed
- **Node.js 18+** (for local frontend development)
- **Python 3.9+** (for local backend development)
- **Git** for version control

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd ecommerce
```

### 2. Start All Services
```bash
# Start all microservices with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps
```

### 3. Access the Platform
- **🎨 Frontend**: http://localhost:3000
- **🔗 GraphQL API**: http://localhost:8000/graphql/
- **⚙️ Django Admin**: http://localhost:8000/admin/
- **📊 Redis**: localhost:6379

## 🧪 Testing the Platform

### GraphQL API Examples

#### Create a User
```bash
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createUser(username: \"john\", email: \"john@example.com\", password: \"123\") { success message user { id username email } } }"
  }'
```

#### Get All Users
```bash
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { users { id username email } }"
  }'
```

#### Create an Order
```bash
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createOrder(userId: 1) { success message order { id status } } }"
  }'
```

### Frontend Testing
1. Open http://localhost:3000 in your browser
2. Navigate through different sections:
   - **Home**: Dashboard with statistics
   - **Users**: Create and manage users
   - **Products**: Browse product catalog
   - **Orders**: Manage orders
3. Test user creation form
4. Test API connectivity

## 🔧 Development

### Local Frontend Development
```bash
cd frontend
npm install
npm start
# Frontend runs on http://localhost:3000
```

### Local Backend Development
```bash
cd api_gateway
pip install -r requirements.txt
python manage.py runserver
# API Gateway runs on http://localhost:8000
```

### Database Migrations
```bash
# User Service
docker-compose exec user_service python -c "from database import create_tables; create_tables()"

# Order Service
docker-compose exec order_service python -c "from database import create_tables; create_tables()"
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api_gateway
docker-compose logs -f user_service
docker-compose logs -f order_service
```

## 🏢 Services Details

### 🌐 API Gateway (Django + GraphQL)
- **Port**: 8000
- **Technology**: Django 4.2, Graphene-Django
- **Purpose**: Unified API layer, request routing, authentication
- **Endpoints**:
  - `GET /graphql/` - GraphQL playground
  - `POST /graphql/` - GraphQL queries and mutations
  - `GET /admin/` - Django admin interface

### 👥 User Service (gRPC)
- **Port**: 50051
- **Technology**: Python gRPC, SQLAlchemy, PostgreSQL
- **Purpose**: User management, authentication, profiles
- **Methods**:
  - `CreateUser` - Register new users
  - `GetUser` - Retrieve user information
  - `UpdateUser` - Update user profiles
  - `DeleteUser` - Remove users

### 🛒 Order Service (gRPC)
- **Port**: 50052
- **Technology**: Python gRPC, SQLAlchemy, PostgreSQL
- **Purpose**: Order processing, inventory management
- **Methods**:
  - `CreateOrder` - Process new orders
  - `GetOrder` - Retrieve order details
  - `ListOrders` - Get user orders
  - `UpdateOrderStatus` - Update order status

### 📊 Supporting Services
- **PostgreSQL Databases**: Separate instances for user and order data
- **Redis**: Caching, session storage, Celery message broker
- **Celery Worker**: Background task processing
- **Nginx**: Production web server (in Docker)

## 🔐 Security Features

- **CORS Protection**: Configured for cross-origin requests
- **CSRF Protection**: Django CSRF middleware
- **SQL Injection Prevention**: SQLAlchemy ORM
- **Input Validation**: GraphQL schema validation
- **Environment Variables**: Sensitive data protection
- **Docker Security**: Isolated containers

## 📈 Performance Features

- **gRPC Communication**: High-performance inter-service calls
- **Redis Caching**: Fast data access
- **Database Indexing**: Optimized queries
- **Async Processing**: Celery for background tasks
- **Connection Pooling**: Efficient database connections
- **Static File Serving**: Nginx for production

## 🚀 Deployment

### Production Deployment
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale user_service=3 --scale order_service=3
```

### Environment Variables
```bash
# .env file
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port/0
ALLOWED_HOSTS=yourdomain.com
```

## 🧪 Testing

### Unit Tests
```bash
# API Gateway tests
docker-compose exec api_gateway python manage.py test

# Service tests
docker-compose exec user_service python -m pytest
docker-compose exec order_service python -m pytest
```

### Integration Tests
```bash
# Test GraphQL endpoints
npm test

# Test gRPC services
python test_grpc_services.py
```

## 📊 Monitoring

### Health Checks
- **API Gateway**: `http://localhost:8000/health/`
- **User Service**: gRPC health check
- **Order Service**: gRPC health check
- **Databases**: PostgreSQL health monitoring
- **Redis**: Redis ping monitoring

### Metrics
- Request/response times
- Database query performance
- Service availability
- Error rates
- Resource usage

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write comprehensive tests
- Update documentation
- Use conventional commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Hechmi** - Full Stack Developer
- Microservices Architecture Specialist
- React & Django Expert
- DevOps Enthusiast

## 🙏 Acknowledgments

- **Django Community** - Amazing web framework
- **React Team** - Revolutionary UI library
- **gRPC Team** - High-performance RPC framework
- **Docker** - Containerization made easy
- **PostgreSQL** - Reliable database system
- **Redis** - Lightning-fast caching

---

⭐ **Star this repository if you found it helpful!**

🐛 **Found a bug?** [Open an issue](https://github.com/your-username/shopflow/issues)

💡 **Have a suggestion?** [Start a discussion](https://github.com/your-username/shopflow/discussions)
