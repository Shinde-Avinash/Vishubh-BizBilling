from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import requests
import os
from django.conf import settings


def generate_invoice_pdf(invoice):
    """Generate PDF for the given invoice"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#00D9A5'),
        spaceAfter=6,
        alignment=TA_CENTER,
    )
    
    company_style = ParagraphStyle(
        'Company',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
    )
    
    # Title
    elements.append(Paragraph("TAX INVOICE", styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Company details
    company_name = getattr(settings, 'COMPANY_NAME', 'Vishubh BizBilling')
    company_address = getattr(settings, 'COMPANY_ADDRESS', '40 Feet road, Pune, Maharashtra 411001')
    company_phone = getattr(settings, 'COMPANY_PHONE', '+91 9890691272')
    company_gstin = getattr(settings, 'COMPANY_GSTIN', '08AALCR2857A1ZD')
    company_pan = getattr(settings, 'COMPANY_PAN', 'AVHPC9999A')
    
    elements.append(Paragraph(f"<b><font color='#00D9A5' size='16'>{company_name}</font></b>", company_style))
    elements.append(Paragraph(company_address, company_style))
    elements.append(Paragraph(f"Phone: {company_phone} &nbsp;&nbsp; GSTIN: {company_gstin} &nbsp;&nbsp; PAN Number: {company_pan}", company_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Customer and invoice details
    customer_invoice_data = [
        [
            Paragraph(f"<b>BILL TO</b><br/>{invoice.customer.name}<br/>{invoice.customer.get_full_address()}<br/>Phone: {invoice.customer.phone}<br/>PAN Number: {invoice.customer.pan_number}<br/>GSTIN: {invoice.customer.gstin}<br/>Place of Supply: {invoice.customer.place_of_supply}", styles['Normal']),
            Paragraph(f"<b>Invoice No</b><br/>{invoice.invoice_number}<br/><br/><b>Invoice Date</b><br/>{invoice.invoice_date.strftime('%d %B %Y')}", styles['Normal'])
        ]
    ]
    
    customer_invoice_table = Table(customer_invoice_data, colWidths=[4*inch, 2*inch])
    customer_invoice_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(customer_invoice_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Invoice items table
    items_data = [
        ['Sr. No.', 'Items', 'Quantity', 'Price / Unit', 'Tax / Unit', 'Amount']
    ]
    
    for idx, item in enumerate(invoice.items.all(), 1):
        items_data.append([
            str(idx),
            item.product.name,
            f"{item.quantity} {item.product.unit}",
            f"Rs. {item.price_per_unit:.2f}",
            f"Rs. {item.tax_amount/item.quantity:.2f} ({item.tax_percentage}%)",
            f"Rs. {item.amount:.2f}"
        ])
    
    # Add discount row
    items_data.append(['', '', '', '', 'Discount', f"Rs. {invoice.discount:.2f}"])
    
    # Add total row
    total_qty = sum(item.quantity for item in invoice.items.all())
    items_data.append(['', 'Total', f"{total_qty:.0f}", '', f"Rs. {invoice.total_tax:.2f}", f"Rs. {invoice.grand_total:.2f}"])
    
    # Add received and due balance
    items_data.append(['', '', 'Received Amount', '', '', f"Rs. {invoice.received_amount:.2f}"])
    items_data.append(['', '', 'Due Balance', '', '', f"Rs. {invoice.due_balance:.2f}"])
    
    items_table = Table(items_data, colWidths=[0.5*inch, 2*inch, 1*inch, 1*inch, 1.2*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00D9A5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, len(items_data)-3), (-1, len(items_data)-3), colors.HexColor('#00D9A5')),
        ('TEXTCOLOR', (0, len(items_data)-3), (-1, len(items_data)-3), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Notes and Terms
    notes_terms_data = [
        [
            Paragraph(f"<b>Notes</b><br/>{invoice.notes or '1. No return deal'}", styles['Normal']),
            Paragraph(f"<b>Terms & Conditions</b><br/>1. Customer will pay the GST<br/>2. Customer will pay the Delivery charges<br/>3. Pay due amount within 15 days", styles['Normal']),
            Paragraph("<b>Authorised Signatory For</b><br/>" + company_name, styles['Normal'])
        ]
    ]
    
    notes_terms_table = Table(notes_terms_data, colWidths=[2*inch, 2.5*inch, 2*inch])
    notes_terms_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(notes_terms_table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


def send_invoice_email(invoice, customer_email):
    """Send invoice PDF to customer via Email (FREE - using Gmail SMTP)"""
    try:
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication
        import smtplib
        
        # Generate PDF
        pdf_buffer = generate_invoice_pdf(invoice)
        
        # Get email settings from settings
        email_host = getattr(settings, 'EMAIL_HOST', 'smtp.gmail.com')
        email_port = getattr(settings, 'EMAIL_PORT', 587)
        email_user = getattr(settings, 'EMAIL_USER', '')
        email_password = getattr(settings, 'EMAIL_PASSWORD', '')
        
        # Remove spaces from app password if present
        if email_password:
            email_password = email_password.replace(' ', '')
        
        if not email_user or not email_password:
            print("Email credentials not configured")
            return False
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = customer_email
        msg['Subject'] = f'Invoice #{invoice.invoice_number} from Vishubh BizBilling'
        
        # Email body
        body = f"""
Dear {invoice.customer.name},

Thank you for your business! Please find attached your invoice.

Invoice Details:
- Invoice Number: {invoice.invoice_number}
- Date: {invoice.invoice_date.strftime('%d %B %Y')}
- Total Amount: Rs. {invoice.grand_total}
- Received Amount: Rs. {invoice.received_amount}
- Due Balance: Rs. {invoice.due_balance}

Best regards,
Vishubh BizBilling Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF
        pdf_attachment = MIMEApplication(pdf_buffer.getvalue(), _subtype='pdf')
        pdf_attachment.add_header('Content-Disposition', 'attachment', 
                                 filename=f'Invoice_{invoice.invoice_number}.pdf')
        msg.attach(pdf_attachment)
        
        # Send email
        server = smtplib.SMTP(email_host, email_port)
        server.starttls()
        server.login(email_user, email_password)
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_invoice_whatsapp(invoice):
    """Send invoice via WhatsApp (OPTIONAL - requires API setup)"""
    try:
        # First generate PDF
        pdf_buffer = generate_invoice_pdf(invoice)
        
        # Get WhatsApp credentials from settings
        phone_number_id = getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', None)
        access_token = getattr(settings, 'WHATSAPP_ACCESS_TOKEN', None)
        
        if not phone_number_id or not access_token:
            print("WhatsApp credentials not configured - Email is recommended")
            return False
        
        # Format customer phone number (remove + and spaces)
        customer_phone = invoice.customer.phone.replace('+', '').replace(' ', '').replace('-', '')
        
        url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Send text message
        message = f"Hello {invoice.customer.name},\n\nYour invoice #{invoice.invoice_number} has been generated.\n\nTotal Amount: Rs. {invoice.grand_total}\nDue Balance: Rs. {invoice.due_balance}\n\nThank you for your business!"
        
        data = {
            "messaging_product": "whatsapp",
            "to": customer_phone,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return True
        else:
            print(f"WhatsApp API error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending WhatsApp: {str(e)}")
        return False
