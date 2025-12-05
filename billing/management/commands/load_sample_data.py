from django.core.management.base import BaseCommand
from billing.models import Product, Customer, Invoice, InvoiceItem
from datetime import datetime, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')
        
        # Create sample products
        products_data = [
            {'name': 'Apple normal', 'category': 'Fruits', 'unit': 'KG', 'price_per_unit': 100.00, 'tax_percentage': 5.00},
            {'name': 'Orange', 'category': 'Fruits', 'unit': 'KG', 'price_per_unit': 40.00, 'tax_percentage': 5.00},
            {'name': 'Banana', 'category': 'Fruits', 'unit': 'DOZEN', 'price_per_unit': 50.00, 'tax_percentage': 5.00},
            {'name': 'Tomato', 'category': 'Vegetables', 'unit': 'KG', 'price_per_unit': 30.00, 'tax_percentage': 5.00},
            {'name': 'Potato', 'category': 'Vegetables', 'unit': 'KG', 'price_per_unit': 25.00, 'tax_percentage': 5.00},
            {'name': 'Onion', 'category': 'Vegetables', 'unit': 'KG', 'price_per_unit': 35.00, 'tax_percentage': 5.00},
            {'name': 'Rice (Basmati)', 'category': 'Grains', 'unit': 'KG', 'price_per_unit': 80.00, 'tax_percentage': 5.00},
            {'name': 'Wheat Flour', 'category': 'Grains', 'unit': 'KG', 'price_per_unit': 45.00, 'tax_percentage': 5.00},
            {'name': 'Milk', 'category': 'Dairy', 'unit': 'LITER', 'price_per_unit': 60.00, 'tax_percentage': 5.00},
            {'name': 'Cooking Oil', 'category': 'Grocery', 'unit': 'LITER', 'price_per_unit': 150.00, 'tax_percentage': 5.00},
        ]
        
        products = []
        for data in products_data:
            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            products.append(product)
            if created:
                self.stdout.write(f'  ✓ Created product: {product.name}')
        
        # Create sample customer
        customer, created = Customer.objects.get_or_create(
            phone='+91 9981028177',
            defaults={
                'name': 'Sampath Singh',
                'address': '04, KK Buildings, Ajmeri Gate',
                'city': 'Jodhpur',
                'state': 'Rajasthan',
                'pincode': '304582',
                'pan_number': 'BBHPC9999A',
                'gstin': '08HULMP2839A1AB',
                'place_of_supply': 'Rajasthan',
            }
        )
        if created:
            self.stdout.write(f'  ✓ Created customer: {customer.name}')
        
        # Create sample invoice
        invoice, created = Invoice.objects.get_or_create(
            invoice_number='S01',
            defaults={
                'customer': customer,
                'invoice_date': datetime.now().date(),
                'discount': Decimal('100.00'),
                'received_amount': Decimal('500.00'),
                'notes': '1. No return deal',
                'terms_conditions': '1. Customer will pay the GST\n2. Customer will pay the Delivery charges\n3. Pay due amount within 15 days',
            }
        )
        
        if created:
            # Add invoice items
            InvoiceItem.objects.create(
                invoice=invoice,
                product=products[0],  # Apple
                quantity=Decimal('5.00'),
            )
            
            InvoiceItem.objects.create(
                invoice=invoice,
                product=products[1],  # Orange
                quantity=Decimal('10.00'),
            )
            
            InvoiceItem.objects.create(
                invoice=invoice,
                product=products[1],  # Orange again
                quantity=Decimal('5.00'),
            )
            
            invoice.calculate_totals()
            self.stdout.write(f'  ✓ Created invoice: {invoice.invoice_number}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sample data loaded successfully!'))
        self.stdout.write(f'\nCreated:')
        self.stdout.write(f'  - {len(products)} products')
        self.stdout.write(f'  - 1 customer')
        self.stdout.write(f'  - 1 sample invoice')
