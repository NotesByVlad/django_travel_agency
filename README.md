# Travel Agency Project

This project is a **Travel Agency Management System** built with **Django**. It allows users to browse and book trips, manage their profiles, and handle bookings dynamically. The system includes features for dynamic pricing, trip and hotel management, meal plans, and more.

---

## 🚀 Project Overview

### Features for Users:
- **Browse Trips**: Users can view available trips.
- **Create Bookings**: Users can create bookings for trips.
- **Profile Management**: Users can view their bookings and have the option to pay for them.
- **Booking History & Invoice**: Once a booking is completed, it appears in the user’s profile with an associated invoice (no actual payment is processed, as this is a simulation).
- **Dynamic Pricing**: Prices for trips are dynamically calculated based on several options selected by the user (e.g., flight options, meal plans, car rentals).

### Features for Admin:
- **Manage Trips**: Admin can create trips with associated hotels, cities, and countries.
- **Trip Details**: Each trip is related to a hotel, which in turn is associated with a city and country. Cities are linked to specific continents.
- **Hotel & City Management**: Admin can add hotels, and each hotel is tied to a city, which has specific details like the airport.
- **Dynamic Cost Calculation**: The cost of a ticket is calculated based on the price of the hotel, the profit margin for adults and children, and flight costs that vary depending on the departure location.
- **Meal Plans**: Hotels offer different meal plans (e.g., no meal plan, BB, HB, FB, AI), and these affect the total cost of the booking.

---

## 🛠️ Running the Project Locally

### Requirements:
- **Python 3.10.0**
- **Django 4.1.1**

### To set up this project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/NotesByVlad/django_travel_agency.git
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - **Windows**:
        ```bash
        .\venv\Scripts\activate
        ```
    - **Mac/Linux**:
        ```bash
        source venv/bin/activate
        ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **📧 Email Setup**:
    
    See [SETUP_EMAIL.md](SETUP_EMAIL.md) for detailed instructions on how to configure the email backend with Gmail's SMTP.
  
 **❓ Troubleshooting**:

- **Common issue: Email not being sent**  
    Make sure you've configured your `.env` and `settings.py` files correctly. Check the SMTP credentials and settings.

- **After setting up your environment and email**

6. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

7. **Create a superuser** (for admin access):
    ```bash
    python manage.py createsuperuser
    ```

8. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

- **Now you can access the app at**: `http://localhost:8000/`.

---

## 📋 Project Features & Architecture

### Trip and Hotel Management:
- Admin can create and manage trips, with each trip being linked to a hotel.
- Hotels have specific attributes like meal plans and prices.
- The cost of a trip is influenced by the selected hotel, flight, and meal plan options.

### Pricing and Meal Plans:
- **Dynamic Pricing**: Prices for trips are dynamically calculated based on:
  - **Hotel Price**: Different hotels can have different price ranges.
  - **Meal Plan**: Meal plans such as Bed and Breakfast, Half Board, FB Full Board, and All-Inclusive can be selected and affect the cost.
  - **Flight Option**: Users can select whether they want a flight or not, with prices varying based on the departure location.
  - **Car Rental**: Car rentals are optional and come with prices that vary by the city.

### Profile and Booking:
- Users can manage their profiles and view their bookings.
- Bookings appear in the user’s profile with an invoice attached (again, no actual payment processing is involved in the project).
- Users can track their booking history and make payments through simulated actions.

---

## 🔒 Authentication Features

- **User Registration**: Users can create accounts.
- **Email Activation**: After registration, users must activate their accounts via an email.
- **Password Reset**: Users can reset their passwords through email.

---

## Why Use Python 3.10.0 and Django 4.1.1?

This project uses **Python 3.10.0** and **Django 4.1.1** for the following reasons:

1. **Stability & Compatibility**  
   - Django 4.1.1 is optimized for Python 3.10 and fully supports its features.  
   - This ensures smooth performance and prevents unexpected behavior.  

2. **Preventing Compatibility Issues**  
   - Some third-party Django packages may not work well with newer Django versions (4.2+).  
   - Using Python 3.11+ could introduce unexpected bugs or deprecated features.  

3. **Course Consistency**  
   - This version is recommended for our course, ensuring that all examples and materials work as expected.  
   - Avoids breaking changes that may exist in newer versions of Django.  

4. **Long-Term Support Considerations**  
   - While Django 4.1 is not an LTS release, it is a stable and widely used version.  
   - Using 4.1.1 provides a balance between new features and reliability.  

By sticking to **Python 3.10.0 + Django 4.1.1**, we ensure a stable, predictable development environment for this project.

# Database Schema
- **Was added with:**
    - django-extensions
    - pyparsing 
    - pydot
    ```bash
    python manage.py graph_models -a -g > my_project.dot
    ```