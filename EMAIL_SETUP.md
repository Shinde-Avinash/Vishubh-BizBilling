# Free Email Setup Guide

## ✅ No Paid API Required!

Instead of using WhatsApp Cloud API (which requires verification and OTP), you can use **FREE Gmail SMTP** to send invoices via email.

## Setup Steps:

### 1. Get Gmail App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in with your Gmail account
3. If asked, enable 2-Step Verification first
4. Select "Mail" app and "Windows Computer" device
5. Click "Generate"
6. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### 2. Update Your `.env` File

Copy `.env.example` to `.env` and update these values:

```bash
# Email Settings (FREE - Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=youremail@gmail.com
EMAIL_PASSWORD=your-16-char-app-password
```

### 3. How to Send Invoices via Email

The system is now configured to send invoices via email instead of WhatsApp!

When you click "Send via WhatsApp" button, it will:
- Generate the invoice PDF
- Send it as an email attachment to the customer
- Customer receives a professional email with:
  - Invoice details in the email body
  - PDF attachment
  - Professional format

## Benefits of Email over WhatsApp:

✅ **100% FREE** - No API costs
✅ **No Verification** - No Facebook Business verification needed
✅ **No OTP Issues** - Works immediately
✅ **Professional** - Email is more professional for invoices
✅ **Reliable** - Gmail SMTP is very reliable
✅ **Attachment Support** - Can send PDF directly
✅ **No Phone Number Required** - Just need customer email

## Troubleshooting:

### "App passwords" option not showing?
- Enable 2-Step Verification first at: https://myaccount.google.com/signinoptions/two-step-verification

### Email not sending?
1. Check that 2-Step Verification is enabled
2. Make sure you're using the App Password, not your regular Gmail password
3. Check EMAIL_USER and EMAIL_PASSWORD are correct in `.env`

### Want to use different email provider?

**Outlook/Hotmail:**
```bash
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USER=youremail@outlook.com
EMAIL_PASSWORD=your-password
```

**Yahoo:**
```bash
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USER=youremail@yahoo.com
EMAIL_PASSWORD=your-app-password
```

## That's it!

You now have a completely FREE invoice sending system with no API costs or verification hassles!
