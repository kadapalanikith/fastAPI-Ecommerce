# FastAPI E-Commerce Application

A robust, high-performance REST API for an e-commerce platform built with Python 3.9+, **FastAPI**, and **Pydantic**. This application manages product information, validates schema inputs with strict business rules, and supports advanced product querying (filtering, sorting, and pagination).

---

## 📂 Project Structure

```text
fastapi-ecommerce/
├── app/
│   ├── data/
│   │   └── products.json          # Mock product database (JSON)
│   ├── schema/
│   │   └── product.py             # Pydantic schemas (Product, Seller) & validators
│   ├── services/
│   │   └── products.py            # Business logic for retrieving product data
│   └── main.py                    # Entry point & API route handlers
├── test/                          # Unit and integration tests
├── readme.md                      # Project documentation (this file)
└── requirements.txt               # Project dependencies
```

---

## 🛠️ Installation & Setup

### 1. Install Dependencies
Ensure you have Python 3.9+ installed. Install the required packages via `pip`:

```bash
pip install -r requirements.txt
```

### 2. Run the Application
Start the Uvicorn development server from the root directory:

```bash
uvicorn fastapi-ecommerce.app.main:app --reload
```

Alternatively, from the `fastapi-ecommerce` directory:

```bash
uvicorn app.main:app --reload
```

### 3. Interactive Documentation
Once the server is running, you can explore the interactive API documentations at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📋 Data Models & Validation

### 1. Seller Model
Stores detailed seller details with restricted email domain checks.
* **Fields**:
  - `id` (UUID): Unique identifier of the seller.
  - `name` (str): Name of the seller (length: 2-60).
  - `email` (EmailStr): Seller email address.
  - `website` (AnyUrl): Link to the seller website.
* **Domain Check (Validator)**:
  - Only email domains `mistore.in` and `hpworld.in` are permitted.

### 2. Product Model
Stores comprehensive product metadata, including pricing, inventory details, and custom validation.
* **Fields**:
  - `id` (UUID): Unique identifier of the product.
  - `sku` (str): Unique Stock Keeping Unit (length: 6-30). *Must contain `-` and end with a 3-digit sequence (e.g., `-234`)*.
  - `name` (str): Name of the product (length: 3-80).
  - `description` (str): Short description (max length: 200).
  - `category` (str): Product category (length: 3-30).
  - `brand` (str): Brand name (length: 2-50).
  - `price` (float): Price of the product in INR (must be > 0).
  - `currency` (Literal["INR"]): Always set to `"INR"`.
  - `discount_percent` (int): Discount rate (0-90%).
  - `stock` (int): Available quantity (>= 0).
  - `is_active` (bool): Indicates if the product is active and visible to buyers.
  - `rating` (float): Product customer rating (0-5).
  - `tags` (list[str], optional): Up to 10 search tags associated with the product.
  - `image_url` (list[AnyUrl]): URLs of product images (maximum 1 URL allowed).
  - `seller` (Seller): Reference to the Seller.
  - `created_at` (datetime): Timestamp when the product was added.

* **Computed Fields**:
  - `final_price` (float): Calculated dynamically as `price * (1 - discount_percent/100)`, rounded to 2 decimal places.

* **Business Rule Validation**:
  - **Stock Check**: If `stock` is `0`, `is_active` must be set to `False`.
  - **Discount Check**: If `discount_percent` is greater than `0`, the product must have a customer rating (`rating > 0`).

---

## 🚀 API Endpoints

### 1. Welcome Root
* **Endpoint**: `GET /`
* **Response**:
  ```json
  {
    "message": "Welcome to the FastAPI E-commerce application!"
  }
  ```

### 2. List & Query Products
* **Endpoint**: `GET /products`
* **Query Parameters**:
  - `name` (str, optional): Search by product name (fuzzy match, case-insensitive).
  - `sort_by_price` (bool, default `false`): Enable sorting products by price.
  - `order` (str, default `"asc"`): Order direction (`"asc"` or `"desc"`).
  - `limit` (int, default `10`): Number of items to return (1 to 100).
  - `offset` (int, default `0`): Pagination offset.
* **Response**:
  ```json
  {
    "total": 45,
    "limit": 10,
    "items": [ ... ]
  }
  ```
* **Status Codes**:
  - `200 OK`: Successful search/fetch.
  - `404 Not Found`: No products matched the search `name`.

### 3. Get Product by ID
* **Endpoint**: `GET /products/{product_id}`
* **Path Parameters**:
  - `product_id` (str, required): The 36-character UUID string of the product.
* **Status Codes**:
  - `200 OK`: Returns the matching product details.
  - `404 Not Found`: No product found with the specified ID.

### 4. Create Product
* **Endpoint**: `POST /products`
* **Request Body**: JSON representing the `Product` schema.
* **Response**: Returns the created product JSON including the computed `final_price`.
* **Status Codes**:
  - `201 Created`: Successfully validated and created.
  - `422 Unprocessable Entity`: Input failed validation checks.

---

## ⚖️ License
This project is licensed under the MIT License.
