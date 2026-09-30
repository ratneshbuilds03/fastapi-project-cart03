# Cart System Backend 🛒

A placement-ready e-commerce backend built with **FastAPI, MySQL, MongoDB, Docker, and JWT authentication**.

The backend provides REST APIs for user authentication, product management, shopping cart operations, and order placement. It uses a dual-database architecture to handle relational and document-oriented application data.

## 🚀 Live API

**Backend API:**
https://cart-system-ylj0.onrender.com

**Swagger / OpenAPI Documentation:**
https://cart-system-ylj0.onrender.com/docs

**Frontend:**
https://cartify-pi-nine.vercel.app/

## ✨ Features

* User registration and login
* JWT-based authentication
* Password validation and authentication
* Product catalog APIs
* Product creation and updates
* Product images
* Shopping cart management
* Checkout and order placement
* MySQL database integration
* MongoDB database integration
* Pydantic request/response validation
* CORS configuration for frontend integration
* Dockerized application
* Swagger / OpenAPI documentation
* Production deployment with Render

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **MySQL**
* **MongoDB**
* **PyMongo / Motor**
* **JWT Authentication**
* **Docker**
* **Docker Compose**
* **Uvicorn**
* **Render**

## 🏗️ Architecture

The application uses a dual-database architecture.

### MySQL

MySQL is used for relational application data such as:

* Users
* Orders
* Authentication-related data

### MongoDB

MongoDB is used for document-oriented application data such as:

* Products
* Shopping cart data

This separation allows each database to handle the type of data it is designed for.

## 🔐 Authentication

The backend provides authentication using JWT tokens.

### Signup

```http
POST /auth/signup
```

Creates a new user account.

### Login

```http
POST /auth/login
```

Authenticates the user using email and password and returns a JWT access token.

The token can then be used for authenticated API requests.

Example:

```http
Authorization: Bearer <access_token>
```

## 📦 Product API

### Get Products

```http
GET /products/
```

Returns the available products.

### Create Product

```http
POST /products/
```

Creates a new product.

Example request:

```json
{
  "name": "Canvas Backpack",
  "description": "Durable everyday backpack",
  "price": 2499,
  "category": "Bags",
  "stock": 20,
  "image": "https://example.com/image.jpg"
}
```

### Update Product

```http
PUT /products/{product_id}
```

Updates an existing product.

Supported product information includes:

* Name
* Description
* Price
* Category
* Stock
* Image

## 🛒 Cart & Order Flow

The backend supports the complete shopping workflow:

```text
Product
   ↓
Add to Cart
   ↓
Cart Management
   ↓
Checkout
   ↓
Place Order
```

The frontend communicates with these backend APIs to provide the complete shopping experience.

## 📚 API Documentation

FastAPI automatically provides interactive Swagger documentation.

**Swagger UI:**

https://cart-system-ylj0.onrender.com/docs

The Swagger interface can be used to explore and test the available REST APIs.

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/ratneshbuilds03/fastapi-project-cart03.git
cd fastapi-project-cart03
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
DATABASE_URL=your_mysql_database_url
MONGODB_URL=your_mongodb_connection_string
MONGODB_DB=cart_db
SECRET_KEY=your_secret_key
```

Do not commit `.env` or any credentials to GitHub.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 🐳 Docker Setup

The backend is Dockerized for consistent development and deployment.

Build and start the application using:

```bash
docker compose up --build
```

The Docker setup can be used to run the backend together with its required database services according to the project configuration.

## 🔑 Environment Variables

| Variable       | Description                            |
| -------------- | -------------------------------------- |
| `DATABASE_URL` | MySQL database connection URL          |
| `MONGODB_URL`  | MongoDB connection string              |
| `MONGODB_DB`   | MongoDB database name                  |
| `SECRET_KEY`   | Secret key used for JWT authentication |

**Never commit real credentials, passwords, connection strings, or secret keys to GitHub.**

## 🌐 Deployment

The backend is deployed using **Render**.

**Production API:**

https://cart-system-ylj0.onrender.com

**Swagger:**

https://cart-system-ylj0.onrender.com/docs

The frontend is deployed separately on Vercel and communicates with this backend through the configured API URL.

## 🔗 Frontend

Cartify frontend:

https://cartify-pi-nine.vercel.app/

Frontend repository:

https://github.com/ratneshbuilds03/cartify-frontend-2s

## 📁 Project Structure

```text
fastapi-project-cart03/
│
├── app/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── models/
│   ├── utils/
│   ├── database.py
│   └── main.py
│
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔄 Application Flow

```text
Client
  │
  ▼
FastAPI REST API
  │
  ├── Authentication
  │      └── JWT
  │
  ├── Products
  │      └── MongoDB
  │
  ├── Cart
  │      └── MongoDB
  │
  └── Orders / Users
         └── MySQL
```

## 🧪 Testing

The project includes backend tests for important application functionality.

Run the test suite with:

```bash
pytest
```

## 🔮 Future Improvements

* Payment gateway integration
* Product search and filtering
* Order history APIs
* Admin dashboard
* Product reviews and ratings
* Advanced inventory management
* Automated CI/CD pipeline improvements

## 📄 License

This project is created for educational, portfolio, and placement purposes.
