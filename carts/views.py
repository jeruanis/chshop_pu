from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from orders.models import Order
from accounts.models import Account
from accounts.forms import CheckoutForm
from currencies.models import Currency
from django.contrib import messages

# Create your views here.
def _cart_id(request): #underscore means that it is private
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    stock = product.stock

    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            #the csrf token is included with its key so we need to explicitely define the keys to find which are size and color or we can start the counting to 1 not zero.
            for item in request.POST:
                key = item
                value = request.POST[key]
                keys = ['color', 'size']
                if key not in keys:
                    continue
                else:
                    try:
                        variation = Variation.objects.get(product=product, variation_category__iexact = key, variation_value__iexact=value)
                        product_variation.append(variation)
                    except Exception as e: #caching the error to continue processing the code
                        messages.warning(request, "There was an error. {}".format(str(e)))

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            existing_variation_list = []
            id_list = []
            # getting the existing variation
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id_list.append(item.id)

            # checking new cart item to existing variation
            if product_variation in existing_variation_list:
                index = existing_variation_list.index(product_variation)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)

                item.quantity += 1
                # check the avilability of the stock
                stock = product.stock
                if (stock-item.quantity) < 0:
                    messages.warning(request, f'You can get only {item.quantity-1}. The stock of {product.product_name} runs out of items already')
                    return redirect('cart')
                else:
                    item.save()

            else:
                #create but if there is variation clear it so they will not mix and just preserve the last one
                item =CartItem.objects.create(product = product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        else: #this is to create an initial item if nothing yet is in the cart (initiator)
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user, #the session key
            )

            #to prevent mixing variations on the manytomanyfield
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            # check the avilability of the stock
            stock = product.stock
            if (stock-cart_item.quantity) < 0:
                messages.warning(request, f'You can get only {cart_item.quantity-1}. The stock of {product.product_name} runs out of items already')
                return redirect('cart')
            else:
                cart_item.save()
        return redirect('cart')

    #if user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                keys = ['color', 'size']
                if key not in keys:
                    continue
                else:
                    try:
                        variation = Variation.objects.get(product=product, variation_category__iexact = key, variation_value__iexact=value)
                        product_variation.append(variation)
                    except Exception as e: #caching the error to continue processing the code
                        messages.warning(request, "There was an error. {}".format(str(e)))

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart using the cart_id in the sesiion
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            #existing variation
            #current variation
            #item id
            existing_variation_list = []
            id_list = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id_list.append(item.id)

            if product_variation in existing_variation_list:
                #just increase
                index = existing_variation_list.index(product_variation)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1

                # check the avilability of the stock
                stock = product.stock
                if (stock-item.quantity) < 0:
                    messages.warning(request, f'You can get only {item.quantity-1}. The stock of {product.product_name} runs out of items already')
                    return redirect('cart')
                else:
                    item.save()

            else:
                #create
                item =CartItem.objects.create(product = product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        else: #this is to create an initial item if nothing yet is in the cart (initiator)
            item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )

            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)

            # check the avilability of the stock
            stock = product.stock
            if (stock-item.quantity) < 0:
                messages.warning(request, f'You can get only {item.quantity}. The stock of {product.product_name} runs out of items already')
                return redirect('cart')
            else:
                item.save()
        return redirect('cart')

def reduce_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(user=request.user, id=cart_item_id)
            #make a condition
            if cart_item.quantity > 1:
                cart_item.quantity -=1
                cart_item.save()
            else:
                cart_item.delete()
        except:
            pass
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request)) #if user is not authenticated
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(user=request.user, id=cart_item_id)
        except:
            pass
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        #inititalize the variable first
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            for cart_item in cart_items:
                total+=(cart_item.product.price*cart_item.quantity)
                quantity+=cart_item.quantity
            tax = (8 * total)/100
            grand_total = total #tax included in the markup
            grand_total = '{:.2f}'.format(float(grand_total))

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

            for cart_item in cart_items:
                total+=(cart_item.product.price*cart_item.quantity)
                quantity+=cart_item.quantity
            tax = (8 * total)/100
            grand_total = total #tax included in the markup
            grand_total = '{:.2f}'.format(float(grand_total))

    except ObjectDoesNotExist:
            pass

    context={'total':total, 'quantity':quantity, 'cart_items':cart_items, 'tax':tax, 'grand_total':grand_total}
    return render(request, 'store/cart.html', context)

@login_required(login_url='login') #need login before going to the page
def checkout(request, total=0, quantity=0, cart_items=None):
    user_details = Account.objects.get(email=request.user)
    form = CheckoutForm(instance = user_details)

    # extract all product category and slug if category and slug match then it will be included in email
    #and put them in dictionary
    eprod = {'cform':'contact_us_form.html', 'lsform':'login_signup_form.zip'}

    #getting the currency
    user = request.user
    accounts = Account.objects.get(email=user)
    country = accounts.country

    if country == 'Philippines':
        currency = 'PHP'
    else:
        currency = 'USD'

    try:
        #inititalize the variable first
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        #summary of computation
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
        tax = (8 * total)/100
        shipping_cost_max = (30 * total)/100

        # do not apply shipping cost for a moment since it will be selling e-products
        #shipping set to minimum /copy this in place_order 2 locations only
        if currency == 'PHP':
            shipping_cost_min = 150
            shipping_cost_applied = max(shipping_cost_max, shipping_cost_min)#get the max value for shipping
            if shipping_cost_applied > 3000:
                shipping_cost = 3000
            else:
                shipping_cost = shipping_cost_applied
        else:
            shipping_cost_min = 8000
            shipping_cost_applied = max(shipping_cost_max, shipping_cost_min)
            if shipping_cost_applied > 8000:
                shipping_cost = 8000
            else:
                shipping_cost = shipping_cost_applied
        # shipping cost end
        shipping_cost = 0;

        grand_total = total + shipping_cost #tax must be included in the markup
        grand_total = '{:.2f}'.format(float(grand_total))

    except ObjectDoesNotExist:
            pass
    context={'total':total, 'quantity':quantity, 'cart_items':cart_items, 'tax':tax, 'grand_total':grand_total,
                'shipping_cost':shipping_cost, 'form':form}
    return render(request, 'store/checkout.html', context)
