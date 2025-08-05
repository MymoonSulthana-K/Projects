from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models # Ensure this import is present for Sum
from django.contrib.auth import login # For the signup view
from django.utils import timezone # For current time/date operations if needed

# Import all your models
from .models import Product, Order, OrderItem, UserProfile, CompostExchange

# Import your forms (assuming CustomUserCreationForm and CompostExchangeForm are in forms.py)
from .forms import CustomUserCreationForm, CompostExchangeForm


# --- Helper Function for Credits (Ensure this is in your views.py) ---
def get_user_credits(user):
    """
    Calculates the total credits earned by a user from compost exchanges.
    """
    return CompostExchange.objects.filter(user=user).aggregate(
        total=models.Sum('credits_earned')
    )['total'] or 0
# --- End Helper Function ---


# Create your views here.
def homepage(request):
    return render(request, "homepage.html")

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save address to profile
            address = form.cleaned_data.get('address')
            UserProfile.objects.create(user=user, address=address)

            login(request, user)
            return redirect('order_veggies')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def order_veggies(request):
    products = Product.objects.all()  # Fetch all products from the database
    cart_items = []
    cart_total = 0

    # Retrieve cart items from the user's session
    cart = request.session.get('cart', {})
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total_price = product.price * quantity
            cart_items.append({'product': product, 'quantity': quantity, 'total_price': total_price})
            cart_total += total_price
        except Product.DoesNotExist:
            # Handle case where product might have been removed
            # This makes the cart robust against deleted products
            if product_id in cart: # Check if it's still there before deleting
                del cart[product_id]
                request.session['cart'] = cart
                request.session.modified = True # Mark session as modified


    context = {
        'products': products,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'order_veggies.html', context)

@login_required(login_url='login')
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        # Use get_object_or_404 to return 404 if product not found
        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get('cart', {})
        # Ensure product_id is stored as a string key for session dictionary consistency
        if str(product_id) in cart:
            cart[str(product_id)] += quantity
        else:
            cart[str(product_id)] = quantity

        request.session['cart'] = cart
        request.session.modified = True  # Important to save session changes

    return redirect('order_veggies')

@login_required(login_url='login')
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            request.session.modified = True

    return redirect('order_veggies')

@login_required(login_url='login')
def clear_cart(request):
    if request.method == 'POST':
        request.session['cart'] = {}
        request.session.modified = True
    return redirect('order_veggies')

@login_required(login_url='login')
def checkout(request):
    if request.method == "POST":
        user = request.user
        session_cart = request.session.get('cart', {})

        if not session_cart:
            return redirect('order_veggies')

        total_price_for_order = Decimal('0.00') # Initialize as Decimal
        order_items_to_create = []

        for product_id_str, quantity in session_cart.items():
            try:
                product_id = int(product_id_str)
                product = Product.objects.get(id=product_id)
                item_total = product.price * quantity
                total_price_for_order += item_total
                order_items_to_create.append({
                    'product': product,
                    'quantity': quantity,
                    'price_at_order': product.price
                })
            except Product.DoesNotExist:
                if product_id_str in session_cart:
                    del session_cart[product_id_str]
                    request.session['cart'] = session_cart
                    request.session.modified = True

        # Calculate discount before creating the order
        total_credits = get_user_credits(request.user)
        discount_value = Decimal(total_credits) # Convert to Decimal
        
        # The discount cannot exceed the order's total price
        # Make sure total_price_for_order is also Decimal, which it is if Product.price is Decimal
        calculated_discount = min(discount_value, total_price_for_order)

        # Create the Order instance, including the discount_applied
        order = Order.objects.create(
            user=user,
            total_price=total_price_for_order,
            discount_applied=calculated_discount # <--- SAVE THE DISCOUNT HERE
        )

        for item_data in order_items_to_create:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                price=item_data['price_at_order']
            )

        # Clear the session cart
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_confirmation', order_id=order.id)
    else:
        return redirect('order_veggies')

from decimal import Decimal
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    profile = UserProfile.objects.filter(user=request.user).first()
    address = profile.address if profile else "No address found for this user."

    order_items = order.items.all()

    # The discount is now stored on the order object itself!
    discount_applied = order.discount_applied
    
    # Calculate the final total using the stored total_price and discount_applied
    final_total_after_discount = order.total_price - discount_applied

    return render(request, 'order_confirmation.html', {
        'order': order,
        'address': address,
        'cart_items': order_items,
        'discount_applied': discount_applied, # This comes directly from the order now
        'cart_total': final_total_after_discount,
    })

@login_required(login_url='login')
def profile(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'profile.html', {
        'user': request.user,
        'orders': orders,
    })


# --- Compost Exchange related views ---
def calculate_credits(kg):
    if kg >= 10:
        return 70
    elif kg >= 5:
        return 30
    elif kg >= 2:
        return 11
    elif kg >= 1:
        return 5
    elif kg >= 0.5:
        return 2
    return 0

@login_required
def compost_exchange(request):
    if request.method == 'POST':
        form = CompostExchangeForm(request.POST)
        if form.is_valid():
            pickup_date = form.cleaned_data['pickup_date']
            compost_amount = form.cleaned_data['compost_amount']
            credits = calculate_credits(compost_amount)

            CompostExchange.objects.create(
                user=request.user,
                pickup_date=pickup_date,
                compost_amount=compost_amount,
                credits_earned=credits
            )
            # Option 1: Redirect to a generic success page (no credits shown on success page itself)
            # return redirect('compost_success')

            # Option 2: Render the compost_exchange page again with an updated credit total and a success message
            # This is often better for immediate feedback without a full redirect
            # You might want to add a message framework for proper success messages
            current_total_credits = get_user_credits(request.user) # Fetch updated credits
            form = CompostExchangeForm() # Clear the form
            return render(request, 'compost_exchange.html', {
                'form': form,
                'total_credits': current_total_credits,
                'success_message': f"Compost submitted! You earned {credits} credits.",
            })
    else:
        form = CompostExchangeForm()

    # Always fetch total credits for GET requests (initial load) and for POST rendering (after submission)
    total_credits = get_user_credits(request.user)

    return render(request, 'compost_exchange.html', {
        'form': form,
        'total_credits': total_credits,
    })