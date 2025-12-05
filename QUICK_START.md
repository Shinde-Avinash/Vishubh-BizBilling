# 🚀 Quick Start Guide - Vishubh BizBilling

## Prerequisites
- Python 3.8 or higher installed
- Internet connection (for first-time setup)

## Installation Steps

### 1. Open PowerShell/Command Prompt
Navigate to the project directory:
```powershell
cd "c:\Users\om\Desktop\TEMP_FILES\2-Avinash\Python\Vishubh BizBilling"
```

### 2. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

If you see a script execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Run the Server
```powershell
python manage.py runserver
```

### 4. Access the Application
Open your browser and go to:
- **Main Application:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## Default Setup

The application comes pre-loaded with:
- ✅ 10 sample products (Apple, Orange, Banana, etc.)
- ✅ 1 sample customer (Sampath Singh)
- ✅ 1 sample invoice (S01)

## Creating Admin User (Optional)

If you want to access the admin panel, create a superuser:
```powershell
python manage.py createsuperuser
```

Follow the prompts and enter:
- Username: admin
- Email: admin@example.com
- Password: (your choice - must be 8+ characters)

## Common Commands

### Start the server:
```powershell
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### Stop the server:
Press `Ctrl + C` in the terminal

### Load more sample data:
```powershell
python manage.py load_sample_data
```

## Features to Try

1. **Product Search**
   - Go to Home page
   - Type product name in search box
   - Click on product to add to cart

2. **Create Invoice**
   - Add products to cart
   - Fill customer information
   - Click "Generate Invoice"

3. **View Invoices**
   - Click "Invoices" in navigation
   - Search by customer name, phone, or invoice number
   - View/Download PDF

4. **Product Management**
   - Click "Products" in navigation
   - Add/Edit/Delete products

5. **Dark/Light Mode**
   - Click the moon/sun icon in top right
   - Toggle between beautiful dark and light themes

## Customization

### Change Company Details
Edit the `.env` file:
```
COMPANY_NAME=Your Business Name
COMPANY_ADDRESS=Your Address
COMPANY_PHONE=Your Phone
COMPANY_GSTIN=Your GSTIN
COMPANY_PAN=Your PAN
```

Restart the server after changes.

## Troubleshooting

### Server won't start?
- Make sure virtual environment is activated
- Check if port 8000 is already in use
- Try different port: `python manage.py runserver 8080`

### Can't see CSS/styling?
- Clear browser cache (Ctrl + Shift + Delete)
- Hard refresh (Ctrl + F5)

### Database errors?
```powershell
python manage.py migrate
```

## Need Help?
Check the full README.md for detailed documentation.

---
**Ready to start billing! 📘**
