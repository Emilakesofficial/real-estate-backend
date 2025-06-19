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
  ![Verify Email](screenshots/verifyemail.png)

- **Resend Email**  
  ![Resend Email](screenshots/resendemail.png)

- **Login / Token**  
  ![Token](screenshots/gettoken.png)

- **Get Profile**  
  ![Get Profile](screenshots/getprofile.png)

- **Update Profile**  
  ![Update Profile](screenshots/updateprofile.png)

- **Change Password Flow**  
  ![Verify Old Password](screenshots/verifyoldpassword.png)  
  ![OTP](screenshots/verifypasswordotp.png)  
  ![Change Password](screenshots/changepassword.png)

### Listings

- **Create Listing**  
  ![Create Property](screenshots/createproperty.png)

- **All Listings**  
  ![All Properties](screenshots/getproperties.png)

- **Single Listing**  
  ![Single Property](screenshots/get_single_property.png)

- **Update / Delete / My Listings**  
  ![Update](screenshots/updateproperty.png)  
  ![Delete](screenshots/deleteproperty.png)  
  ![My Properties](screenshots/getmyproperties.png)

### Inquiries

- **Make Inquiry**  
  ![Make Inquiry](screenshots/usermakeenquiry.png)

- **View Inquiries (Renter/Buyer)**  
  ![Renter View](screenshots/viewenquiryrenter.png)

- **View & Reply (Agent)**  
  ![Agent View](screenshots/viewenquiryagent.png)  
  ![Reply](screenshots/replyenquiryagent.png)

### Checkout & Payment

- **Cart**  
  ![Add to Cart](screenshots/addtocart.png)  
  ![Remove from Cart](screenshots/removefromcart.png)  
  ![Get Cart](screenshots/getcart.png)

- **Payment**  
  ![Initialize](screenshots/initializepayment.png)  
  ![Verify](screenshots/verifypayment.png)


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