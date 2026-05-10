# sales/views.py  — complete file with authentication applied to all views

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .forms import OrderItemForm


@login_required
def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'sales/product_list.html', {'products': products})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'sales/product_detail.html', {'product': product})


@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'sales/order_list.html', {'orders': orders})


@login_required
def create_order(request):
    """Instantly create an open order and jump straight to the add-items page."""
    order = Order.objects.create(
        cashier=request.user,
        status='open',
    )
    return redirect('add_item', pk=order.pk)


@login_required
def add_item(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        if 'mark_paid' in request.POST:
            order.status = 'paid'
            order.save()
            return redirect('order_list')
        item_form = OrderItemForm(request.POST)
        if item_form.is_valid():
            item            = item_form.save(commit=False)
            item.order      = order
            item.unit_price = item.product.price
            item.save()
            return redirect('add_item', pk=order.pk)
    else:
        item_form = OrderItemForm()
    return render(request, 'sales/add_item.html', {
        'order': order,
        'item_form': item_form,
        'items': order.items.select_related('product'),
    })
