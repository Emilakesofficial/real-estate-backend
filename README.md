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

## 🛠 Tech Stack

- **Backend**: Django + Django REST Framework
- **Auth**: JWT (Simple JWT)
- **Payments**: Paystack API
- **Docs**: Swagger (drf-yasg)
- **DB**: SQLite (easily swappable to Postgres/MySQL)

---

## 📘 API Documentation

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
  ![Verify Email](screenshots/verify_email.png)

- **Resend Email**  
  ![Resend Email](screenshots/resend_email.png)

- **Login / Token**  
  ![Token](screenshots/get_token.png)

- **Get Profile**  
  ![Get Profile](screenshots/get_profile.png)

- **Update Profile**  
  ![Update Profile](screenshots/update_profile.png)

- **Change Password Flow**  
  ![Verify Old Password](screenshots/verify_old_password.png)  
  ![OTP](screenshots/verify_password_otp.png)  
  ![Change Password](screenshots/change_password.png)

### Listings

- **Create Listing**  
  ![Create Property](screenshots/create_property.png)

- **All Listings**  
  ![All Properties](screenshots/get_properties.png)

- **Single Listing**  
  ![Single Property](screenshots/get_single_property.png)

- **Update / Delete / My Listings**  
  ![Update](screenshots/update_property.png)  
  ![Delete](screenshots/delete_property.png)  
  ![My Properties](screenshots/get_my_properties.png)

### Inquiries

- **Make Inquiry**  
  ![Make Inquiry](screenshots/user_make_enquiry.png)

- **View Inquiries (Renter/Buyer)**  
  ![Renter View](screenshots/view_enquiry_renter.png)

- **View & Reply (Agent)**  
  ![Agent View](screenshots/view_enquiry_agent.png)  
  ![Reply](screenshots/reply_enquiry_agent.png)

### Checkout & Payment

- **Cart**  
  ![Add to Cart](screenshots/add_to_cart.png)  
  ![Remove from Cart](screenshots/remove_from_cart.png)  
  ![Get Cart](screenshots/get_cart.png)

- **Payment**  
  ![Initialize](screenshots/initialize_payment.png)  
  ![Verify](screenshots/verify_payment.png)


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