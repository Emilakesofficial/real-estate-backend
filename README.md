# Real Estate API

A fully-featured Real Estate backend built with Django REST Framework. Supports agent and renter/buyer roles, property listings, inquiries, JWT authentication, and Paystack integration.

---

## Features

-  **JWT Authentication** with email verification
-  **Agent & Renter/Buyer Roles**
-  **Agents can list, view, update and delete their properties**
-  **Renters/Buyers can browse listings**
-  **Messaging system** for inquiries and responses between renters and agents
-  **Integrated Paystack payments** for renting/buying properties
-  **Profile management** with image upload
-  Country & role selection on registration
-  API organized across 4 Django apps:
- `users`: registration, login, profile, etc.
- `listings`: property management
- `checkout`: cart & purchase logic
- `payment`: Paystack integration

---

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Payment**: Paystack API
- **API Documentation**: Swagger (drf-yasg)
- **Database**: SQLite (default, changeable to Postgres/MySQL)

---

## API Documentation

Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)  
ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## Sample API Endpoints

| Feature       | Endpoint                        | Method |
|---------------|----------------------------------|--------|
| Register      | `/api/users/register/`           | POST   |
| Login         | `/token/`                        | POST   |
| Listings      | `/api/listings/get/properties/`  | GET    |
| Create Listing| `/api/listings/create/property/` | POST   |
| Make Inquiry  | `/api/listings/enquire/`         | POST   |
| Payment       | `/api/payment/initialize/`       | POST   |

## Screenshots
## ENDPOINTS

## register
![alt text](register.png)

## verify email
![alt text](<verify email.png>)

## resend email
![alt text](<resend email.png>)

## token
![alt text](<get token.png>)

## login
![alt text](login.png)

## get profile
![alt text](<get profile.png>)

## update profile
![alt text](<update profile.png>)

## verify old password
![alt text](<verify old password.png>)

## verify old password otp
![alt text](<verify password otp.png>)

## change password
![alt text](<change password.png>)

### forget password 
![alt text](image.png)

### verify-forget-password-otp
![alt text](verify-forget-password-otp.png)

### reset password
![alt text](<reset password.png>)

### Listings

### Create listing
![alt text](<create property.png>)

### View all listings
![alt text](<get properties.png>)

### View single listing
![alt text](<get single property.png>)

### update property(only agent who listed the property can update)
![alt text](<update property.png>)

### delete property
![alt text](<delete property.png>)

### get my properties(agent)
![alt text](<get my properties(agent).png>)

### Inquiries

### make enquiry
![alt text](<user make enquiry.png>)

### view replied and all enquiries(renter/buyer)
![alt text](<view enquiry(renterbuyer).png>)

### view all enquiries(agent)
![alt text](<view enquiry(agent).png>)

### reply enquiries(agent)
![alt text](<reply enquiry (agent).png>)

### Checkout & Payment

### add to cart
![alt text](<add to cart.png>)

### remove from cart
![alt text](<remove from cart.png>)

### get cart
![alt text](<get cart.png>)

- **Payment**

### initialize payment
![alt text](<initialize payment.png>)

### verify payment
![alt text](<verify payment.png>)

> Full documentation with request/response formats is available on Swagger UI.

---

## Setup Instructions

1. **Clone the repo**  
   ```bash
   git clone https://github.com/Emilakesofficial/real-estate-backend.git
   cd real-estate-backend

2. **Create and activate a virtual environment**
    python -m venv venv
    source venv/bin/activate  # on Windows: venv\Scripts\activate

3. **Install dependencies**
    pip install -r requirements.txt

4.**Run migrations**
    python manage.py migrate

5. **Start the server**
    python manage.py runserver




