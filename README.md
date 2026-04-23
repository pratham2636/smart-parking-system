# 🚗 Smart Parking System

A web-based **Smart Parking System** built using **Flask & MySQL** that allows users to find and book parking slots online, while providing an admin panel to manage parking spaces and monitor bookings.

---

## ✨ Features

### 👤 User Side

* 🔐 User Registration & Login
* 🚗 View Available Parking Slots
* 📅 Book Parking Slot (Start & End Time)
* 💰 Automatic Price Calculation (₹10 per hour)
* ⏰ Expiry Alerts for bookings
* 📖 View Booking History
* 👤 Profile Management
* 🔒 Change Password

---

### 👑 Admin Side

* 📊 Dashboard (Users, Bookings, Revenue)
* ➕ Add New Parking
* ✏️ Edit Parking Details
* ❌ Delete Parking
* 📉 Manage Slot Availability

---

### 💳 Payment

* 💰 Simulated Payment System (UPI / Card UI)
* 💵 Booking amount calculated based on duration

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, Bootstrap
* **Backend:** Flask (Python)
* **Database:** MySQL
* **Tools:** MySQL Workbench, PyCharm

---

## 📂 Project Structure

```
smart-parking-system/
│
├── app.py
├── smart_parking.sql
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── parkings.html
│   ├── book.html
│   ├── payment.html
│   ├── my_bookings.html
│   ├── profile.html
│   ├── edit_profile.html
│   ├── change_password.html
│   └── admin.html
│
└── README.md
```

---

## 🗄️ Database Setup

1. Open **MySQL Workbench**
2. Create a new database (optional name: `smart_parking`)
3. Import the file:

```
smart_parking.sql
```

4. All tables and data will be created automatically

---

## ▶️ How to Run

1. Install required packages:

```
pip install flask mysql-connector-python
```

2. Run the application:

```
python app.py
```

3. Open browser and go to:

```
http://127.0.0.1:5000
```

---



## 💡 Key Highlights

* ⏱️ Real-time slot availability handling
* 🔄 Automatic booking expiry logic
* 💰 Dynamic pricing based on time
* 🧠 Smart slot allocation system
* 📦 Complete database dump included

---

## 👨‍💻 Author

**Pratham Joshi**

---

## 📌 Note

* This project is for educational purposes
* Payment system is simulated (no real transactions)
* Uses Bootstrap CDN (no static folder required)

---

## 🚀 Future Improvements

* Real payment gateway integration (Razorpay / Stripe)
* Google Maps integration
* Email notifications
* Mobile app version

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
