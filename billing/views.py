from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
import json

from .models import Product, Customer, Invoice, InvoiceItem
from .utils import generate_invoice_pdf, send_invoice_whatsapp, send_invoice_email


def index(request):
    """Landing page with product search and cart"""
    return render(request, 'billing/index.html')


@require_http_methods(["GET"])
def search_products(request):
    """AJAX endpoint for searching products"""
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'products': []})
    
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(category__icontains=query),
        is_active=True
    )[:10]
    
    products_data = [{
        'id': p.id,
        'name': p.name,
        'category': p.category,
        'unit': p.unit,
        'price_per_unit': float(p.price_per_unit),
        'tax_percentage': float(p.tax_percentage),
    } for p in products]
    
    return JsonResponse({'products': products_data})


def product_list(request):
    """Product CRUD - List view"""
    products = Product.objects.all()
    return render(request, 'billing/product_list.html', {'products': products})


def product_create(request):
    """Product CRUD - Create view"""
    if request.method == 'POST':
        product = Product(
            name=request.POST['name'],
            category=request.POST.get('category', ''),
            unit=request.POST['unit'],
            price_per_unit=Decimal(request.POST['price_per_unit']),
            tax_percentage=Decimal(request.POST['tax_percentage']),
        )
        product.save()
        return redirect('product_list')
    
    return render(request, 'billing/product_form.html', {
        'unit_choices': Product.UNIT_CHOICES
    })


def product_update(request, pk):
    """Product CRUD - Update view"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.name = request.POST['name']
        product.category = request.POST.get('category', '')
        product.unit = request.POST['unit']
        product.price_per_unit = Decimal(request.POST['price_per_unit'])
        product.tax_percentage = Decimal(request.POST['tax_percentage'])
        product.save()
        return redirect('product_list')
    
    return render(request, 'billing/product_form.html', {
        'product': product,
        'unit_choices': Product.UNIT_CHOICES
    })


def product_delete(request, pk):
    """Product CRUD - Delete view (Soft Delete)"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.is_active = False
        product.save()
        return redirect('product_list')
    
    return render(request, 'billing/product_confirm_delete.html', {'product': product})


def generate_invoice(request):
    """Generate invoice from cart data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get or create customer
            customer_data = data['customer']
            customer, created = Customer.objects.get_or_create(
                email=customer_data['email'],
                defaults={
                    'name': customer_data['name'],
                    'phone': '',
                    'address': '-',
                    'city': '-',
                    'state': 'India',
                    'pincode': '000000',
                    'pan_number': '',
                    'gstin': '',
                    'place_of_supply': 'India',
                }
            )
            
            # Generate invoice number
            last_invoice = Invoice.objects.order_by('-invoice_number').first()
            if last_invoice and last_invoice.invoice_number.startswith('S'):
                try:
                    last_num = int(last_invoice.invoice_number[1:])
                    invoice_number = f"S{last_num + 1:02d}"
                except:
                    invoice_number = f"S01"
            else:
                invoice_number = "S01"
            
            # Create invoice
            invoice = Invoice.objects.create(
                invoice_number=invoice_number,
                customer=customer,
                invoice_date=datetime.now().date(),
                discount=Decimal(data.get('discount', 0)),
                received_amount=Decimal(data.get('received_amount', 0)),
                notes=data.get('notes', ''),
                terms_conditions=data.get('terms_conditions', ''),
            )
            
            # Create invoice items
            for item_data in data['items']:
                product = Product.objects.get(id=item_data['product_id'])
                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=Decimal(item_data['quantity']),
                )
            
            # Calculate totals
            invoice.calculate_totals()
            
            # Auto-send email
            email_sent = False
            if customer.email:
                email_sent = send_invoice_email(invoice, customer.email)
                if email_sent:
                    invoice.email_sent = True
                    invoice.email_sent_at = timezone.now()
                    invoice.save()
            
            return JsonResponse({
                'success': True,
                'invoice_id': invoice.id,
                'invoice_number': invoice.invoice_number,
                'email_sent': email_sent,
                'customer_email': customer.email
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def invoice_detail(request, pk):
    """View invoice detail and download PDF"""
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})


def invoice_pdf(request, pk):
    """Generate and download invoice PDF"""
    invoice = get_object_or_404(Invoice, pk=pk)
    pdf_buffer = generate_invoice_pdf(invoice)
    
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{invoice.invoice_number}.pdf"'
    
    return response


def invoice_search(request):
    """Search invoices by customer name, phone, or invoice number"""
    query = request.GET.get('q', '').strip()
    
    invoices = Invoice.objects.all().order_by('-created_at')
    
    if query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=query) |
            Q(customer__name__icontains=query) |
            Q(customer__phone__icontains=query)
        )
    
    return render(request, 'billing/invoice_search.html', {
        'invoices': invoices,
        'query': query
    })



def send_invoice_to_whatsapp(request, pk):
    """Send invoice to customer's WhatsApp"""
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        try:
            success = send_invoice_whatsapp(invoice)
            
            if success:
                invoice.whatsapp_sent = True
                invoice.whatsapp_sent_at = datetime.now()
                invoice.save()
                
                return JsonResponse({'success': True, 'message': 'Invoice sent successfully!'})
            else:
                return JsonResponse({'success': False, 'error': 'Failed to send WhatsApp message'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def send_invoice_to_email(request, pk):
    """Send invoice to customer's Email (FREE)"""
    from .utils import send_invoice_email
    
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_email = data.get('email', '')
            
            if not customer_email:
                return JsonResponse({'success': False, 'error': 'Email address is required'})
            
            success = send_invoice_email(invoice, customer_email)
            
            if success:
                invoice.email_sent = True
                invoice.email_sent_at = timezone.now()
                invoice.save()
                return JsonResponse({'success': True, 'message': f'Invoice sent successfully to {customer_email}!'})
            else:
                return JsonResponse({'success': False, 'error': 'Failed to send email. Please check email configuration.'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def statistics(request):
    """View for business statistics dashboard"""
    # Overall Totals
    total_revenue = Invoice.objects.aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    pending_payments = Invoice.objects.aggregate(Sum('due_balance'))['due_balance__sum'] or 0
    total_invoices = Invoice.objects.count()
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    
    # Monthly Stats
    now = timezone.now()
    current_month_invoices = Invoice.objects.filter(
        invoice_date__year=now.year,
        invoice_date__month=now.month
    )
    month_revenue = current_month_invoices.aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    month_invoices_count = current_month_invoices.count()
    
    # Recent Invoices
    recent_invoices = Invoice.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_revenue': total_revenue,
        'pending_payments': pending_payments,
        'total_invoices': total_invoices,
        'total_products': total_products,
        'total_customers': total_customers,
        'month_revenue': month_revenue,
        'month_invoices_count': month_invoices_count,
        'recent_invoices': recent_invoices,
    }
    return render(request, 'billing/statistics_v2.html', context)
