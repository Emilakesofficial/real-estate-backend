# Real Estate API

A fully-featured Real Estate backend built with Django REST Framework. Supports agent and renter/buyer roles, property listings, inquiries, JWT authentication, and Paystack integration.

---

## Features

-  JWT Authentication with Email Verification
-  Agent & Renter/Buyer Roles
-  Agents can Create, View, Update & Delete Listings
-  Renters/Buyers can Browse Listings
-  Messaging System for Inquiries and Responses
-  Integrated Paystack Payments for Renting/Buying
-  Profile Management with Image Upload
-  Country & Role Selection during Registration
-  Modular Architecture using Django Apps:
  - `users` – registration, login, profile, etc.
  - `listings` – property management
  - `checkout` – cart system
  - `payment` – Paystack integration

---

##  Tech Stack

- **Backend**: Django + Django REST Framework
- **Auth**: JWT (Simple JWT)
- **Payments**: Paystack API
- **Docs**: Swagger (drf-yasg)
- **DB**: SQLite (easily swappable to Postgres/MySQL)

---

## API Documentation

- [Swagger UI](http://localhost:8000/swagger/)
- [ReDoc](http://localhost:8000/redoc/)

---

## Sample Endpoints

| Feature       | Endpoint                        | Method |
|---------------|----------------------------------|--------|
| Register      | `/api/users/register/`           | POST   |
| Login         | `/token/`                        | POST   |
| Listings      | `/api/listings/get/properties/`  | GET    |
| Create Listing| `/api/listings/create/property/` | POST   |
| Make Inquiry  | `/api/listings/enquire/`         | POST   |
| Payment       | `/api/payment/initialize/`       | POST   |


## Screenshots

### Auth & User

- **Register**  
  ![Register](screenshots/register.png)

- **Verify Email**  
  ![Verify Email](screenshots/verify%20email.png)

- **Resend Email**  
  ![Resend Email](screenshots/resend%20email.png)

- **Login / Token**  
  ![Token](screenshots/get%20token.png)

- **Get Profile**  
  ![Get Profile](screenshots/get%20profile.png)

- **Update Profile**  
  ![Update Profile](screenshots/update%20profile.png)

- **Change Password Flow**  
  ![Verify Old Password](screenshots/verify%20old%20password.png)  
  ![OTP](screenshots/verify%20password%20otp.png)  
  ![Change Password](screenshots/change%20password.png)

### Listings

- **Create Listing**  
  ![Create Property](screenshots/create%20property.png)

- **All Listings**  
  ![All Properties](screenshots/get%20properties.png)

- **Single Listing**  
  ![Single Property](screenshots/get%20single%20property.png)

- **Update / Delete / My Listings**  
  ![Update](screenshots/update%20property.png)  
  ![Delete](screenshots/delete%20property.png)  
  ![My Properties](screenshots/get%20my%20properties(agent).png)

### Inquiries

- **Make Inquiry**  
  ![Make Inquiry](screenshots/user%20make%20enquiry.png)

- **View Inquiries (Renter/Buyer)**  
  ![Renter View](screenshots/view%20enquiry(renterbuyer).png)

- **View & Reply (Agent)**  
  ![Agent View](screenshots/view%20enquiry(agent).png)  
  ![Reply](screenshots/reply%20enquiry%20(agent).png)

### Checkout & Payment

- **Cart**  
  screenshots/add to cart.png 
  ![Remove from Cart](screenshots/remove%20from%20cart.png)  
  ![Get Cart](screenshots/get%20cart.png)

- **Payment**  
  ![Initialize](screenshots/initialize%20payment.png)  
  ![Verify](screenshots/verify%20payment.png)


## Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/Emilakesofficial/real-estate-backend.git
cd real-estate-backend

# 2. Create & activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Run server
python manage.py runserver


**Contact**
For inquiries or collaboration:
📧 adegbemiadekunle56@gmail.com
🔗 LinkedIn : https://www.linkedin.com/in/adekunle-adegbemi-4b590a346?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app