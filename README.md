# CoreInventory Management System

A robust Inventory Management System built with Flask, MySQL, and Tailwind CSS. Featuring full authentication, stock tracking, and automated reporting.

## 🚀 Key Features

- **Inventory Tracking:** Real-time monitoring of stock levels, on-hand qty, and reserved stock.
- **Stock Moves:** Efficient management of Receipts (Incoming), Deliveries (Outgoing), and Internal Transfers.
- **Authentication:** Secure login/signup system with password strength validation and OTP-based password reset.
- **Auto-Seeding:** Automatic database table creation and dummy data population for new setups.
- **Responsive Design:** Premium UI with Glassmorphism, animations, and dark/light modes.

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Frontend:** HTML5, Javascript, Tailwind CSS
- **Notifications:** Flask-Mail (Gmail Integration)

## 📋 Prerequisites

- Python 3.8+
- MySQL Server (running locally)

## ⚙️ Installation & Setup

1. **Clone the repository** (or copy files to your directory).
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Database:**
   - Create a database named `core_inventory` in your MySQL server.
   - The app is configured for `root` with no password by default (edit `app.py` if needed).
4. **Configure Email (for OTP):**
   - Open `email_config.py`.
   - Update `MAIL_USERNAME` with your Gmail address.
   - Update `MAIL_PASSWORD` with your **16-character App Password**.
5. **Run the Application:**
   ```bash
   python app.py
   ```

## 📂 Project Structure

- `app.py`: Main entry point and auto-seed logic.
- `auth_routes.py`: Handles login, logout, and password resets.
- `models.py`: Database schema definitions.
- `seed_users.py`: Independent script for multi-user dummy data (if needed).
- `templates/`: HTML templates for all pages.
- `static/`: CSS and JS assets.

## 💡 Automated Data Seeding

On the first run, CoreInventory will automatically:
1. Create all necessary database tables.
2. Seed master data (Warehouses, Locations, Products, Contacts).
3. Populate dummy transactions for demo users **Maithil (User 4)** and **Myth12 (User 5)**.

---
© 2026 CoreInventory Management System.
