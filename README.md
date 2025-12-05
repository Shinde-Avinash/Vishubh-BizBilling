# 📘 Vishubh BizBilling — Smart Invoice Generator & Product Management System

A lightweight, professional business billing system built with Python, Django, and SQLite. Features a modern dark/light mode UI with glassmorphism effects and smooth animations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📌 Project Overview

Vishubh BizBilling is a simple yet powerful billing and inventory management application designed for small and medium businesses. It allows shop owners to:

- ✅ Search & add products to a cart with live AJAX search
- ✅ Generate professional GST-style tax invoices (PDF/print format)
- ✅ Maintain a product database through a CRUD admin panel
- ✅ Search previous bills for returning customers
- ✅ Send invoices directly to customer's WhatsApp using WhatsApp Cloud API
- ✅ Toggle between beautiful dark and light themes

## 🧰 Tech Stack

- **Backend:** Python 3.8+, Django 4.2.7
- **Database:** SQLite
- **Frontend:** Django Templates, HTML5, CSS3, JavaScript (Vanilla)
- **PDF Generation:** ReportLab
- **WhatsApp Integration:** WhatsApp Cloud API
- **Styling:** Custom CSS with CSS Variables, Glassmorphism, Modern Gradients

## 🗂️ Core Features

### 1️⃣ Landing Page (Product Search + Cart System)
- Live product search using name or category
- AJAX-based instant search results
- Add/remove items to cart
- Adjust quantity with automatic price, tax, discount & total calculation
- Proceed to generate bill

### 2️⃣ Product CRUD Panel
Users can:
- ➕ Add new shop items
- 📝 Update products
- ❌ Delete products
- 📋 View complete item list

Product fields include:
- Item name
- Category
- Unit (KG, Piece, Liter, etc.)
- Price per unit
- Tax percentage

### 3️⃣ Invoice Search & History
- Search past bills by customer name, mobile number, or invoice number
- View complete invoice details
- Reprint or download PDF
- Check returning customers' purchase history
- Track payment status (received amount, due balance)

### 4️⃣ WhatsApp Invoice Sending
After generating the bill, the system can:
- Convert the invoice into a PDF
- Automatically send the invoice to customer's WhatsApp number using WhatsApp Cloud API
- Track which invoices have been sent

### 5️⃣ Beautiful UI with Dark/Light Mode
- Modern, premium design with vibrant colors
- Smooth theme toggle between dark and light modes
- Glassmorphism effects and modern gradients
- Responsive design for all devices
- Micro-animations for enhanced UX

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd "Vishubh BizBilling"
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and update the following:
```
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Company Details (customize for your business)
COMPANY_NAME=Akash Enterprises
COMPANY_ADDRESS=Ajmer Road, Jaipur, Rajasthan 301202
COMPANY_PHONE=+91 9981278197
COMPANY_GSTIN=08AALCR2857A1ZD
COMPANY_PAN=AVHPC9999A

# WhatsApp Cloud API Settings (optional, for WhatsApp feature)
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_ACCESS_TOKEN=your-access-token
WHATSAPP_BUSINESS_ACCOUNT_ID=your-business-account-id
```

### Step 6: Run Migrations
```bash
python manage.py migrate
```

### Step 7: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 8: Run Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

Admin panel: **http://127.0.0.1:8000/admin/**

## 📚 Usage Guide

### Adding Products
1. Navigate to **Products** page
2. Click **Add New Product**
3. Fill in product details:
   - Name (e.g., "Apple", "Orange")
   - Category (e.g., "Fruits", "Vegetables")
   - Unit (KG, Piece, etc.)
   - Price per unit
   - Tax percentage
4. Click **Add Product**

### Creating an Invoice
1. Go to **Home** page
2. Search for products using the search bar
3. Click on products to add them to cart
4. Adjust quantities as needed
5. Fill in customer information
6. Set discount and received amount (optional)
7. Click **Generate Invoice**

### Searching Invoices
1. Navigate to **Invoices** page
2. Use the search bar to find invoices by:
   - Invoice number
   - Customer name
   - Phone number
3. View, download PDF, or send via WhatsApp

### Sending Invoice via WhatsApp
1. View an invoice detail page
2. Click **Send WhatsApp** button
3. Invoice will be sent to customer's phone number
(Note: Requires WhatsApp Cloud API configuration)

## 🎨 Theme Toggle

The application features a beautiful dark/light mode toggle:
- Click the theme toggle button (🌙/☀️) in the navbar
- Theme preference is saved in browser localStorage
- Smooth transitions between themes
- Premium design in both modes

## 📄 Invoice Format

Generated invoices match professional GST tax invoice standards with:
- Company details (name, address, GSTIN, PAN)
- Customer information (name, address, GSTIN, PAN)
- Invoice number and date
- Itemized product list with quantities, prices, and taxes
- Subtotal, tax total, discount, and grand total
- Received amount and due balance
- Notes and terms & conditions
- Authorized signatory section

## 🔧 Configuration

### Customizing Company Details
Edit the `.env` file to update your company information:
```
COMPANY_NAME=Your Business Name
COMPANY_ADDRESS=Your Address
COMPANY_PHONE=Your Phone Number
COMPANY_GSTIN=Your GSTIN
COMPANY_PAN=Your PAN Number
```

### WhatsApp Integration Setup
To enable WhatsApp sending:
1. Create a WhatsApp Business Account
2. Get your Phone Number ID and Access Token from Meta Business Suite
3. Update `.env` with your credentials

## 📁 Project Structure
```
Vishubh BizBilling/
├── billing/                 # Main app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   └── utils.py            # PDF & WhatsApp utilities
├── bizbilling/             # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/              # HTML templates
│   ├── base.html
│   └── billing/
├── static/                 # Static files
│   ├── css/
│   │   └── style.css      # Complete design system
│   └── js/
│       └── app.js         # JavaScript logic
├── manage.py
├── requirements.txt
├── .env                    # Environment variables
└── README.md
```

## 🌟 Key Features Highlight

✔️ **Generate GST-style tax invoice** matching professional standards
✔️ **Auto-total calculations** for subtotal, tax, discount, and balance
✔️ **Discount and payment tracking** with received amount & balance
✔️ **Customer information section** with full GST compliance
✔️ **WhatsApp integration** for modern bill delivery
✔️ **Save all bills in database** for record keeping
✔️ **Reprint past bills anytime**
✔️ **Clean, modern, and premium UI**
✔️ **Dark/Light theme toggle**
✔️ **Full product inventory CRUD**
✔️ **Responsive design** for all devices

## 🚀 Why Vishubh BizBilling?

- **Easy to use** for day-to-day shop billing
- **Local SQLite database** for fast performance
- **Professional invoice output** matching industry standards
- **WhatsApp sending** makes it modern like real POS systems
- **Premium UI** with dark/light mode for comfortable use
- **Easy to extend** with barcode scanning, POS printer support, GST reports, etc.

## 📝 License

This project is open source and available under the MIT License.

## 👥 Support

For issues, questions, or contributions, please create an issue in the repository.

---

**Built with ❤️ for small businesses**
