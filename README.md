# CoreInventory - Comprehensive Inventory Management System

CoreInventory is a full-stack Inventory Management System (IMS) designed to help businesses efficiently track their stock levels, manage warehouses, and handle logistics operations seamlessly. Built with Python, Flask, and MySQL, it offers a fast, reliable, and user-friendly interface.

## 🚀 Features

* **User Management:** Secure authentication with password hashing and OTP-based password resets via email.
* **Dashboard Analytics:** Visual overview of current stock limits, recent moves, and inventory standing.
* **Inventory Tracking:** Real-time visibility into stock availability across different warehouses and specific locations.
* **Product Catalog:** Manage items, track unit costs, and link to inventory dynamically.
* **Warehouses & Locations:** Easily track and manage multi-warehouse operations down to the individual shelf or bin location.
* **Stock Operations**
  * **Receipts:** Record incoming stock from vendors.
  * **Deliveries:** Manage outgoing shipments to customers.
  * **Internal Transfers:** Move inventory physically between warehouse locations internally.
* **Contacts Directory:** A central hub to manage vendor and customer details.

## 🛠️ Technology Stack

* **Backend:** Python 3.10+, Flask, Flask-SQLAlchemy, Werkzeug
* **Database:** MySQL (via PyMySQL connector)
* **Frontend:** HTML5, CSS3, JavaScript, Jinja2 Templating
* **Email System:** Simple SMTP-based setup for OTP using Flask-Mail

## 📋 Prerequisites

To run this application locally, you will need:
* Python 3.8 or higher
* MySQL Server (XAMPP/WAMP can be used for local development)

## 🔧 Installation & Setup

1. **Clone the project** (or download and extract the source code):
   ```bash
   git clone <your-repository-url>
   cd CoreInventory
   ```

2. **Set up a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration:**
   * Start your MySQL server and create a database named `core_inventory`.
   * The application connects to a MySQL DB with `root` user and no password on `localhost` by default. To alter this behaviour, edit the connection string inside `app.py`:
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/core_inventory'
     ```
   * You can simply run `python seed_users.py` and `python seed_data.py` to populate initial demo data and automatically create your tables! Alternatively, an SQL dump is provided.

5. **Email Configuration (for OTP/password recovery):**
   * Edit `email_config.py` in the root folder.
   * Add your Google Mail configuration / App password as specified within the file to perform e-mail password recovery tests.

6. **Run the Application:**
   ```bash
   python app.py
   # OR
   flask run
   ```
   * Access the dashboard at `http://127.0.0.1:5000`

## 🤝 Contributing

Contributions are always welcome! Feel free to fork the repository, make changes, and open a Pull Request.

## 📝 License

This project is open-source and available under the terms of the MIT License.
