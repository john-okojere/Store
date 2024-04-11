from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from shelf.models import Product, Sizes
from .models import Cart, CartItem, Payment, Order
from .forms import AddToCartForm, UpdateCartItemForm

import random
import string

@login_required
def add_to_cart(request, product_uid):
    product = get_object_or_404(Product, uid=product_uid)
    if request.method == 'POST':
        form = AddToCartForm(request.POST, product=product)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            info = form.cleaned_data['info'] # Handle case where 'info' is not provided
            sizes_selected = [key.split('_')[1] for key, value in form.cleaned_data.items() if key.startswith('size_') and value]
            if len(sizes_selected) > 1 and quantity == 1:
                return JsonResponse({'success': False, 'errors': 'You cannot select more than one size if the quantity is one.'}, status=400)
            
            cart, created = Cart.objects.get_or_create(user=request.user, cleared=False)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, info=info)
            cart_item.quantity += quantity
            cart_item.save()
            cart_item.size.set(Sizes.objects.filter(id__in=sizes_selected))
            print(info)  # Assign selected sizes to the cart item
            print(form.cleaned_data.items())  # Assign selected sizes to the cart item
            return JsonResponse({'success': True, 'message': 'Product added to cart successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)


@login_required
def delete_from_cart(request, cart_item_uid):
    try:
        cart_item = get_object_or_404(CartItem, uid=cart_item_uid)
        cart_item.delete()
        return redirect('view_cart')  # Redirect to the cart view after deleting the item
    except CartItem.DoesNotExist:
        # If the cart item does not exist, return to the cart view with an error message
        return redirect('view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user, cleared= False)
    cart_items = cart.cartitem_set.all()
    total = sum(item.subtotal() for item in cart_items)

    
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items,'total': total, 'cart':cart})

@login_required
def update_cart_item(request, cart_item_uid):
    cart_item = get_object_or_404(CartItem, uid=cart_item_uid)
    if request.method == 'POST':
        form = UpdateCartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('view_cart')
    else:
        form = UpdateCartItemForm(instance=cart_item)
    return render(request, 'cart/view_cart.html', {'form': form, 'cart/cart_item': cart_item})

from .models import Payment
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Cart, Payment

@login_required
def initiate_payment(request):
    cart, created = Cart.objects.get_or_create(user=request.user, cleared=False)
    cart_items = cart.cartitem_set.all()
    total = sum(item.subtotal() for item in cart_items)
    
    if request.method == "POST":
        # Extract shipping address details from the form
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone_number = request.POST.get('phone_number')
        
        # Extract email from the form
        email = request.POST.get('email')
        
        # Create a payment object with shipping address and email
        payment = Payment.objects.create(
            amount=total,
            email=email,
            cart = cart,
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            state=state,
            phone_number=phone_number
        )
        payment.save()
        
        # Pass necessary context to the payment template
        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
            'amount_value': payment.amount_value(),
        }
        
        # Render the payment template with the context
        return render(request, 'make_payment.html', context)

    # Render the initial payment form template
    return render(request, 'payment.html', {'cart': cart, 'total': total})

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render

def sm(request):
    
 
    return redirect('/')
       


def verify_payment(request, ref):
    payment = Payment.objects.get(ref=ref)
    cart = payment.cart
    cart_items = payment.cart.cartitem_set.all()
    total = sum(item.subtotal() for item in cart_items)
    order = Order.objects.filter(payment=payment)
    if order:
        order = Order.objects.get(payment=payment)
    if payment.amount == total:
        verified = payment.verify_payment()
    else:
        verified = False

    if verified:
        cart = payment.cart
        cart.cleared = True
        cart.save()
        sender = "store@layersoftruth.org"

        # Send email to buyer
        buyer_email = request.user.email
        buyer_subject = 'Order Confirmation'
        buyer_message = render_to_string('order_confirmation_email.html', {'cart_items': cart_items, 'total': total,'cart': cart,'payment': payment,'order':order})
        send_mail(buyer_subject, strip_tags(buyer_message), sender, [buyer_email], html_message=buyer_message)

        # Send email to seller
        seller_email = sender # Assuming seller email is stored in the Order model
        seller_subject = 'New Order Received'
        seller_message = render_to_string('new_order_email.html', {'cart_items': cart_items, 'total': total,'cart': cart,'payment': payment,'order':order})
        send_mail(seller_subject, strip_tags(seller_message), sender, [seller_email], html_message=seller_message)


        print(request.user, " ordered successfully")
        return render(request, "success.html",  {'cart_items': cart_items, 'total': total,'cart': cart,'payment': payment,'order':order})
            
    return render(request, "success.html", {'cart_items': cart_items,'total': total,'cart': cart,'payment': payment,'order':order})


def payment_history(request):
    payment = Payment.objects.filter(verified = True)
    return render(request, "payment_history.html", {'payments': payment,})

def sent_order(request, ref):
    payment = Payment.objects.get(ref=ref)
    order = Order.objects.get(payment=payment)
    order.sent = True
    order.save()
    cart_items = payment.cart.cartitem_set.all()
    total = sum(item.subtotal() for item in cart_items)
    cart = payment.cart
    return render(request, "success.html",  {'cart_items': cart_items, 'total': total,'cart': cart,'payment': payment,'order':order})


def order_delivered(request, ref):
    payment = Payment.objects.get(ref=ref)
    order = Order.objects.get(payment=payment)
    order.delivered = True
    order.save()
    cart_items = payment.cart.cartitem_set.all()
    total = sum(item.subtotal() for item in cart_items)
    cart = payment.cart
    return render(request, "success.html",  {'cart_items': cart_items, 'total': total,'cart': cart,'payment': payment,'order':order})