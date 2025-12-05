// =============================================
// Vishubh BizBilling - Main JavaScript
// =============================================

// Theme Management
class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.applyTheme(this.theme);
        this.setupToggleButton();
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.theme = theme;
        localStorage.setItem('theme', theme);
        this.updateToggleButton();
    }

    toggle() {
        const newTheme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    }

    setupToggleButton() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggle());
        }
    }

    updateToggleButton() {
        const toggleBtn = document.getElementById('theme-toggle');
        const icon = toggleBtn?.querySelector('.theme-toggle-icon');
        if (icon) {
            icon.textContent = this.theme === 'light' ? '🌙' : '☀️';
        }
    }
}

// Product Search
class ProductSearch {
    constructor(inputId, resultsId) {
        this.input = document.getElementById(inputId);
        this.results = document.getElementById(resultsId);
        this.debounceTimer = null;
        this.init();
    }

    init() {
        if (!this.input || !this.results) return;

        this.input.addEventListener('input', (e) => {
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(() => {
                this.search(e.target.value);
            }, 300);
        });

        // Close results when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-container')) {
                this.results.style.display = 'none';
            }
        });
    }

    async search(query) {
        if (!query || query.length < 2) {
            this.results.style.display = 'none';
            return;
        }

        try {
            const response = await fetch(`/api/search-products/?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            this.displayResults(data.products);
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    displayResults(products) {
        if (!products || products.length === 0) {
            this.results.innerHTML = '<div class="search-result-item">No products found</div>';
            this.results.style.display = 'block';
            return;
        }

        this.results.innerHTML = products.map(product => `
            <div class="search-result-item" onclick="cart.addProduct(${JSON.stringify(product).replace(/"/g, '&quot;')})">
                <div style="font-weight: 600;">${product.name}</div>
                <div style="font-size: 0.875rem; color: var(--text-secondary);">
                    ${product.category || 'Uncategorized'} - Rs. ${product.price_per_unit}/${product.unit}
                </div>
            </div>
        `).join('');

        this.results.style.display = 'block';
    }
}

// Shopping Cart
class ShoppingCart {
    constructor() {
        this.items = [];
        this.discount = 0;
        this.receivedAmount = 0;
    }

    addProduct(product) {
        const existingItem = this.items.find(item => item.id === product.id);

        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.items.push({
                ...product,
                quantity: 1
            });
        }

        this.render();
        this.hideSearchResults();
    }

    removeProduct(productId) {
        this.items = this.items.filter(item => item.id !== productId);
        this.render();
    }

    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.id === productId);
        if (item) {
            item.quantity = parseFloat(quantity) || 0;
            if (item.quantity <= 0) {
                this.removeProduct(productId);
            } else {
                this.render();
            }
        }
    }

    calculateItemTotal(item) {
        const baseAmount = item.price_per_unit * item.quantity;
        const taxAmount = (baseAmount * item.tax_percentage) / 100;
        return baseAmount + taxAmount;
    }

    calculateSubtotal() {
        return this.items.reduce((sum, item) => {
            return sum + (item.price_per_unit * item.quantity);
        }, 0);
    }

    calculateTotalTax() {
        return this.items.reduce((sum, item) => {
            const baseAmount = item.price_per_unit * item.quantity;
            return sum + ((baseAmount * item.tax_percentage) / 100);
        }, 0);
    }

    calculateGrandTotal() {
        const subtotal = this.calculateSubtotal();
        const tax = this.calculateTotalTax();
        return subtotal + tax - this.discount;
    }

    calculateDueBalance() {
        return this.calculateGrandTotal() - this.receivedAmount;
    }

    setDiscount(amount) {
        this.discount = parseFloat(amount) || 0;
        this.render();
    }

    setReceivedAmount(amount) {
        this.receivedAmount = parseFloat(amount) || 0;
        this.render();
    }

    render() {
        const cartItemsEl = document.getElementById('cart-items');
        const cartSummaryEl = document.getElementById('cart-summary');

        if (!cartItemsEl || !cartSummaryEl) return;

        // Render cart items
        if (this.items.length === 0) {
            cartItemsEl.innerHTML = '<div class="text-center text-muted p-4">Cart is empty</div>';
        } else {
            cartItemsEl.innerHTML = this.items.map((item, index) => `
                <div class="cart-item">
                    <div style="flex: 1;">
                        <div style="font-weight: 600;">${item.name}</div>
                        <div style="font-size: 0.875rem; color: var(--text-secondary);">
                            Rs. ${item.price_per_unit.toFixed(2)}/${item.unit} + ${item.tax_percentage}% tax
                        </div>
                    </div>
                    <div style="display: flex; gap: 1rem; align-items: center;">
                        <input 
                            type="number" 
                            value="${item.quantity}" 
                            min="0.01" 
                            step="0.01"
                            onchange="cart.updateQuantity(${item.id}, this.value)"
                            style="width: 80px; padding: 0.5rem; border: 2px solid var(--border-color); border-radius: 8px; background: var(--bg-secondary); color: var(--text-primary);"
                        />
                        <div style="font-weight: 600; min-width: 100px; text-align: right;">
                            Rs. ${this.calculateItemTotal(item).toFixed(2)}
                        </div>
                        <button 
                            onclick="cart.removeProduct(${item.id})"
                            class="btn btn-danger btn-sm"
                            style="padding: 0.5rem;"
                        >
                            ×
                        </button>
                    </div>
                </div>
            `).join('');
        }

        // Render summary
        const subtotal = this.calculateSubtotal();
        const tax = this.calculateTotalTax();
        const grandTotal = this.calculateGrandTotal();
        const dueBalance = this.calculateDueBalance();

        cartSummaryEl.innerHTML = `
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                <span>Subtotal:</span>
                <span style="font-weight: 600;">Rs. ${subtotal.toFixed(2)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                <span>Tax:</span>
                <span style="font-weight: 600;">Rs. ${tax.toFixed(2)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                <span>Discount:</span>
                <input 
                    type="number" 
                    value="${this.discount}" 
                    min="0" 
                    step="0.01"
                    onchange="cart.setDiscount(this.value)"
                    style="width: 120px; padding: 0.5rem; border: 2px solid var(--border-color); border-radius: 8px; background: var(--bg-secondary); color: var(--text-primary); text-align: right; font-weight: 600;"
                />
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-top: 2px solid var(--border-color); margin-top: 0.5rem;">
                <span style="font-size: 1.25rem; font-weight: 700;">Grand Total:</span>
                <span style="font-size: 1.25rem; font-weight: 700; color: var(--brand-primary);">Rs. ${grandTotal.toFixed(2)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                <span>Received Amount:</span>
                <input 
                    type="number" 
                    value="${this.receivedAmount}" 
                    min="0" 
                    step="0.01"
                    onchange="cart.setReceivedAmount(this.value)"
                    style="width: 120px; padding: 0.5rem; border: 2px solid var(--border-color); border-radius: 8px; background: var(--bg-secondary); color: var(--text-primary); text-align: right; font-weight: 600;"
                />
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                <span>Due Balance:</span>
                <span style="font-weight: 700; color: ${dueBalance > 0 ? 'var(--accent-red)' : 'var(--brand-primary)'};">
                    Rs. ${dueBalance.toFixed(2)}
                </span>
            </div>
        `;
    }

    hideSearchResults() {
        const searchResults = document.getElementById('search-results');
        if (searchResults) {
            searchResults.style.display = 'none';
        }
    }

    clear() {
        this.items = [];
        this.discount = 0;
        this.receivedAmount = 0;
        this.render();
    }

    getCartData() {
        return {
            items: this.items.map(item => ({
                product_id: item.id,
                quantity: item.quantity
            })),
            discount: this.discount,
            received_amount: this.receivedAmount
        };
    }
}

// Toast Notification
function showToast(message, type = 'success', duration = 10000) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type} fade-in`;
    toast.style.cssText = `
        background: ${type === 'success' ? 'var(--brand-primary)' : 'var(--accent-red)'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        min-width: 300px;
        z-index: 10000;
    `;

    const icon = type === 'success' ? '✅' : '❌';
    toast.innerHTML = `
        <span style="font-size: 1.2rem;">${icon}</span>
        <div style="font-weight: 500;">${message}</div>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Invoice Generation
async function generateInvoice() {
    const customerForm = document.getElementById('customer-form');

    if (!customerForm) {
        alert('Customer form not found');
        return;
    }

    // Validate form
    if (!customerForm.checkValidity()) {
        customerForm.reportValidity();
        return;
    }

    // Validate cart
    if (cart.items.length === 0) {
        alert('Please add items to cart');
        return;
    }

    // Get customer data
    const formData = new FormData(customerForm);
    const customerData = {
        name: formData.get('name'),
        email: formData.get('email'),
        phone: '',
        address: formData.get('address'),
        city: formData.get('city'),
        state: formData.get('state'),
        pincode: formData.get('pincode'),
        pan_number: formData.get('pan_number') || '',
        gstin: formData.get('gstin') || '',
        place_of_supply: formData.get('place_of_supply') || formData.get('state')
    };

    // Prepare invoice data
    const invoiceData = {
        customer: customerData,
        ...cart.getCartData(),
        notes: formData.get('notes') || '',
        terms_conditions: formData.get('terms_conditions') || '1. Customer will pay the GST\n2. Customer will pay the Delivery charges\n3. Pay due amount within 15 days'
    };

    const btn = document.getElementById('generate-btn');
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '⏳ Generating & Sending Email...';

    try {
        const response = await fetch('/invoice/generate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(invoiceData)
        });

        const data = await response.json();

        if (data.success) {
            // Redirect to invoice detail with email status
            window.location.href = `/invoice/${data.invoice_id}/?email_sent=${data.email_sent}&customer_email=${encodeURIComponent(data.customer_email || '')}`;
        } else {
            alert('Error: ' + (data.error || 'Unknown error occurred'));
            btn.disabled = false;
            btn.innerHTML = originalText;
        }
    } catch (error) {
        console.error('Error generating invoice:', error);
        alert('Failed to generate invoice');
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize on page load
let themeManager;
let productSearch;
let cart;

document.addEventListener('DOMContentLoaded', function () {
    // Initialize theme manager
    themeManager = new ThemeManager();

    // Initialize product search if on main page
    if (document.getElementById('product-search')) {
        productSearch = new ProductSearch('product-search', 'search-results');
    }

    // Initialize cart if on main page
    if (document.getElementById('cart-items')) {
        cart = new ShoppingCart();
        cart.render();
    }
});
