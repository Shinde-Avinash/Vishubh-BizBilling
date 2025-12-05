from django.contrib import admin
from .models import Product, Customer, Invoice, InvoiceItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_per_unit', 'unit', 'tax_percentage', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'unit']
    search_fields = ['name', 'category']
    list_editable = ['is_active']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'city', 'state', 'created_at']
    search_fields = ['name', 'phone', 'gstin', 'pan_number']
    list_filter = ['state', 'city']


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    readonly_fields = ['tax_amount', 'amount']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'invoice_date', 'grand_total', 'due_balance', 'whatsapp_sent']
    list_filter = ['invoice_date', 'whatsapp_sent']
    search_fields = ['invoice_number', 'customer__name', 'customer__phone']
    readonly_fields = ['subtotal', 'total_tax', 'grand_total', 'due_balance']
    inlines = [InvoiceItemInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.calculate_totals()
