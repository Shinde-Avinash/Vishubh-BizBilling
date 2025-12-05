from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Product(models.Model):
    """Model for storing product/item information"""
    UNIT_CHOICES = [
        ('KG', 'Kilogram'),
        ('PIECE', 'Piece'),
        ('LITER', 'Liter'),
        ('METER', 'Meter'),
        ('BOX', 'Box'),
        ('DOZEN', 'Dozen'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='PIECE')
    price_per_unit = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    tax_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=5.00,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - Rs. {self.price_per_unit}/{self.unit}"
    
    def get_tax_amount(self, quantity):
        """Calculate tax amount for given quantity"""
        base_amount = self.price_per_unit * Decimal(quantity)
        return (base_amount * self.tax_percentage) / Decimal('100')
    
    def get_total_amount(self, quantity):
        """Calculate total amount including tax"""
        base_amount = self.price_per_unit * Decimal(quantity)
        tax_amount = self.get_tax_amount(quantity)
        return base_amount + tax_amount


class Customer(models.Model):
    """Model for storing customer information"""
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    pan_number = models.CharField(max_length=10, blank=True)
    gstin = models.CharField(max_length=15, blank=True)
    place_of_supply = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.email or self.phone}"
    
    def get_full_address(self):
        """Return formatted full address"""
        return f"{self.address}, {self.city}, {self.state}, {self.pincode}"


class Invoice(models.Model):
    """Model for storing invoice/bill information"""
    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    invoice_date = models.DateField()
    
    # Totals
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    received_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Additional info
    notes = models.TextField(blank=True)
    terms_conditions = models.TextField(blank=True)
    
    # WhatsApp
    whatsapp_sent = models.BooleanField(default=False)
    whatsapp_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Email
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-invoice_date', '-invoice_number']
    
    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.customer.name}"
    
    def calculate_totals(self):
        """Calculate all totals based on invoice items"""
        items = self.items.all()
        
        self.subtotal = sum((item.get_base_amount() for item in items), Decimal('0'))
        self.total_tax = sum((item.tax_amount for item in items), Decimal('0'))
        
        total_before_discount = self.subtotal + self.total_tax
        self.grand_total = total_before_discount - self.discount
        self.due_balance = self.grand_total - self.received_amount
        
        self.save()


class InvoiceItem(models.Model):
    """Model for storing individual items in an invoice"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_base_amount(self):
        """Calculate amount without tax"""
        return self.price_per_unit * self.quantity

    def get_tax_per_unit(self):
        """Calculate tax per unit"""
        return (self.price_per_unit * self.tax_percentage) / Decimal('100')
    
    def save(self, *args, **kwargs):
        """Override save to auto-calculate amounts"""
        # Store current product values
        self.price_per_unit = self.product.price_per_unit
        self.tax_percentage = self.product.tax_percentage
        
        # Calculate amounts
        base_amount = self.get_base_amount()
        self.tax_amount = (base_amount * self.tax_percentage) / Decimal('100')
        self.amount = base_amount + self.tax_amount
        
        super().save(*args, **kwargs)
