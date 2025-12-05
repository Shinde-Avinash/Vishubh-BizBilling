from django.urls import path
from . import views

urlpatterns = [
    # Landing page
    path('', views.index, name='index'),
    
    # Product search API
    path('api/search-products/', views.search_products, name='search_products'),
    
    # Product CRUD
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Invoice operations
    path('invoice/generate/', views.generate_invoice, name='generate_invoice'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('invoice/<int:pk>/whatsapp/', views.send_invoice_to_whatsapp, name='send_whatsapp'),
    path('invoice/<int:pk>/email/', views.send_invoice_to_email, name='send_email'),
    
    # Invoice search
    path('invoices/search/', views.invoice_search, name='invoice_search'),
    
    # Statistics
    path('statistics/', views.statistics, name='statistics'),
]
