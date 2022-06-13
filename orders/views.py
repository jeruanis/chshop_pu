from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem, Cart
from carts.views import _cart_id
from .forms import OrderForm, OrderStatusForm
import datetime
from .models import Order, OrderProduct, Payment
import json
from store.models import Product
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from currencies.models import Currency
from accounts.decorators import allowed_users
import decimal
from decimal import Decimal

from decouple import config
from twilio.rest import Client
from shopme.settings import EMAIL_HOST_USER

from shopme import settings

#place_order and payments have the same html template called payments
@login_required(login_url='login')
def payments(request):

    #loading the content of the body
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    #store transaction details inside payment models
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],

    )
    payment.save()

    #update the payment database
    order.payment = payment
    #update the is_ordered status
    order.is_ordered = True #order is_ordered setting to true
    order.save()

    #Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)
    # catch the product slugs
    product_slug = []
    #assign the items to the OrderProducts table
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.total_price = item.quantity * item.product.price
        orderproduct.ordered = True #ordereproduct setting ordered to true
        orderproduct.ip = request.META.get('REMOTE_ADDR')
        orderproduct.save()

        #get the id generated after saving orderproduct
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct.variation.set(product_variation)
        #update orderproduct for product_variation
        orderproduct.save()

        #Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)

        product_slug.append(product.slug)

        product.stock -= item.quantity
        product.sold +=item.quantity
        product.save()

    #clear cart and CartItms
    cart_items = CartItem.objects.filter(user=request.user)#total user cart_items
    # cart_id_used = []
    # for item in cart_items:
    #     cart_id_used.append(item.cart)

    # cart = Cart.objects.filter(cart_id=cart_id_used[0])
    cart_items.delete()
    # cart.delete()

    #removing unexecuted orders in the database
    is_orders_not_executed = Order.objects.filter(user = request.user, is_ordered=False).exists()
    if is_orders_not_executed:
        orders_not_executed = Order.objects.filter(user = request.user, is_ordered=False)
        for old_orders in orders_not_executed:
            old_orders.delete()
    else:
        pass

    #need to convert here since in email is not covered by the currency converter so provide a factor fr conversion
    user = request.user
    accounts = Account.objects.get(email=user)
    country = accounts.country
    if country == 'Philippines':
        currency = 'PHP'
    else:
        currency = 'USD'
    current_currency = Currency.objects.get(code=currency)

    if currency != 'PHP':
        factor = current_currency.factor
    else:
        factor=1

    order_total = order.order_total
    amount_total = Decimal(order_total)*factor #must be both decimal
    amount_total = '{:.2f}'.format(Decimal(amount_total))

    # for product with attachments start
    prod_code_dict = {'cform':'contact_us.html', 'lsform':['jvstore.png', 'sign_up_form.html']}
    slug_list = ['cform', 'lsform']

    # eproduct listing path
    listFpath = []
    for slug in product_slug:
        if slug in slug_list:
            listFpath.append(slug)
        else:
            continue

    # print('listFpath', listFpath)
    true_path = []
    for key, value in prod_code_dict.items():
        for item in listFpath:
            if(item == key):
                fpath = value
                true_path.append(fpath)
            else:
                continue

    #Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user':request.user,
        'order':order,
        'currency':currency,
        'amount_total':amount_total

    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, EMAIL_HOST_USER, [to_email], [EMAIL_HOST_USER])

    # for local testing use
    # send_email.attach_file(settings.STATIC_ROOT+'/assets/contact_us_form/contact_us.html')

    # for production use. for product attachment
    f_length = len(true_path)
    # print('f_length', f_length)
    if(f_length == 1): # one item bought
        if(true_path[0] == 'contact_us.html'):
            send_email.attach_file(settings.STATICFILES_DIRS[0] + '/assets/eforms/' + true_path[0])
        else:
            send_email.attach_file(settings.STATICFILES_DIRS[0] + '/assets/eforms/login_signup/' + true_path[0][0], 'image/png')
            send_email.attach_file(settings.STATICFILES_DIRS[0] + '/assets/eforms/login_signup/' + true_path[0][1], 'text/html')

    elif(f_length == 2): #2 items bought
        if(true_path[0] == 'contact_us.html'):
            send_email.attach_file(settings.STATICFILES_DIRS[0] + '/assets/eforms/' + true_path[0])
            send_email.attach_file(settings.STATICFILES_DIRS[0] + '/assets/eforms/login_signup/' + true_path[1][0], 'image/png')
            send_email.attach_file(settings.STATICFILES_DIRS[0] + '/assets/eforms/login_signup/' + true_path[1][1], 'text/html')
        else:
            send_email.attach_file(settings.STATICFILES_DIRS[0] + '/assets/eforms/login_signup/' + true_path[0][0], 'image/png')
            send_email.attach_file(settings.STATICFILES_DIRS[0] + '/assets/eforms/login_signup/' + true_path[0][1], 'text/html')
            send_email.attach_file(settings.STATICFILES_DIRS[0] + '/assets/eforms/' + true_path[1])

    send_email.send()

    #Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    #TWILIO
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    # account_sid = config('account_sid')
    # auth_token = config('auth_token')
    # client = Client(account_sid, auth_token)
    #
    # message = client.messages \
    #                 .create(
    #                      body="Hello Jerwin, you just have a new order:" + payment.payment_id,
    #                      from_='+12075158271',
    #                      to = config('to')
    #                  )
    #
    # print(message.sid)
    return JsonResponse(data)


@login_required(login_url='login')
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    #get other details from the two items above
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)
        if payment.status == 'COMPLETED':
            pay_status = 'PAID'
        else:
            pay_status = payment.status

        subtotal = 0
        #looping through the product items
        for i in ordered_products:
            subtotal+=i.product_price*i.quantity

        context = {
            'order': order_number,
            'ordered_products': ordered_products,
            'order_number': order_number,
            'transID': payment.payment_id,
            'orderDate': order.created_at,
            'status': order.status,
            'payment': payment,
            'order': order,
            'pay_status':pay_status,
            'sub_total':subtotal,


        }
        return render(request, 'orders/order_complete.html', context)

    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


@login_required(login_url='login')
def place_order(request, total=0, quantity=0):
    current_user = request.user

    #if the cart count is 0 redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total=0
    tax = 0

    #getting the currency
    user = request.user
    accounts = Account.objects.get(email=user)
    country = accounts.country
    if country == 'Philippines':
        currency = 'PHP'
    else:
        currency = 'USD'

    #summary of computation
    for cart_item in cart_items:
        total+=(cart_item.product.price*cart_item.quantity)
        quantity+=cart_item.quantity
    tax = (8 * total)/100
    #get the location and provide the shipping for that location
    shipping_cost_max = (30 * total)/100

    #shipping set to minimum /similar to checkout 2 locations only
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

    # override the shipping cost to zero
    shipping_cost = 0;

    grand_total = total + shipping_cost #tax must be included in the markup
    grand_total ='{:.2f}'.format(Decimal(grand_total)) #reduce to 2 decimal places


    if request.method == 'POST':
        form = OrderForm(request.POST)
        zip = request.POST['zip']
        address_line_1 = request.POST['address_line_1']
        if not zip:
            messages.warning(request, 'ZIP is missing!. Suggestion: Update later your ZIP code via edit profile.')
            return redirect('checkout')
        if not address_line_1:
            messages.warning(request, 'Address Line 1 is missing!. Suggestion: Complete later your Address via edit profile. To prevent this warning in the future. Thank you.')
            return redirect('checkout')

        if form.is_valid():
            #store all the billing information indside Order table
            data = Order() #initiate Order class
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.zip = form.cleaned_data['zip']
            data.currency = form.cleaned_data['currency']
            data.item_count = form.cleaned_data['item_count']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.shipping = shipping_cost
            data.tax = tax #static
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            #Generate order number
            y = int(datetime.date.today().strftime('%Y'))
            d = int(datetime.date.today().strftime('%d'))
            m = int(datetime.date.today().strftime('%m'))
            dt = datetime.date(y,m,d)
            current_date = dt.strftime("%Y%m%d") #20210305
            #then cocatenate the primary key to current_date

            #data.id is generated upon saving
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            #declare that order is still false
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context={
                'order':order, 'cart_items': cart_items, 'tax':tax, 'total':total, 'grand_total':grand_total, 'shipping_cost':shipping_cost
                }
            return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')

    else:
        return redirect('checkout')


@login_required(login_url='login')
def order_detail(request, order_number):
    order = Order.objects.get(order_number=order_number)
    payment_id = order.payment
    ordered_products = OrderProduct.objects.filter(payment=payment_id)

    payment = Payment.objects.get(payment_id=payment_id)
    if payment.status == 'COMPLETED':
        pay_status = 'PAID'
    else:
        pay_status = payment.status

    subtotal = 0
    #looping through the product items
    for i in ordered_products:
        subtotal+=i.product_price*i.quantity

    #getting the currency sysmbol
    if order.currency == 'PHP':
        order_symbol = '₱'
    else:
        currency = 'USD'
        order_symbol = '$'

    context = {
        'ordered_products': ordered_products,
        'order_number': order_number,
        'transID': payment.payment_id,
        'orderDate': order.created_at,
        'status': order.status,
        'payment': payment,
        'order': order,
        'pay_status':pay_status,
        'sub_total':subtotal,
        'order_symbol':order_symbol
    }

    return render(request, 'orders/order_detail.html', context)

#for seller only
@login_required(login_url='login')
@allowed_users(allowed_roles=['Seller'])
def update_order_status(request, pk):
    user = request.GET.get('usr')
    transID = request.GET.get('trans')
    pr_name = request.GET.get('pr')

    # Specify specific prduct
    orderproduct = OrderProduct.objects.filter(ordered=True, payment__payment_id=pk, product__slug=pr_name)

    # since there is no instance. then cannot assign instance in the form except putting fisrt()
    form = OrderStatusForm(instance=orderproduct.first())
    if request.user.is_authenticated:
        if request.method == 'POST':
            for item in orderproduct:
                form = OrderStatusForm(request.POST, instance=item)
                if form.is_valid():
                    form.save()

            messages.success(request, 'Successfully updated the Order Status.')
            return redirect('my_store_order')
        context = {'form': form, 'transID':transID}
        return render(request, 'orders/update_order_status.html', context)
    else:
        messages.warning(request, 'Access not permitted!')
        return redirect('store')



#for admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_status_cancel(request, pk):
    ops = request.GET.get('ops')
    order = OrderProduct.objects.filter(order__order_number=pk, product__slug=ops)
    if request.user.is_authenticated:
        if request.method == 'POST':
            status = request.POST['cancel']
            if status == 'cancelled':
                for order in order:
                    order.status = 'Done Refund'
                    order.is_refund = True
                    order.save()
            messages.success(request, 'Successfully refund.')
            return redirect('dashboard_single')
    else:
        messages.warning(request, 'Access not permitted!')
        return redirect('store')



#for customer
@login_required(login_url='login')
# in case seller also can buy products he can delete
@allowed_users(allowed_roles=['Customer', 'Seller'])
def deleted_order(request, pk):
    if request.user.is_authenticated:
        opsref = request.GET.get('opsref')
        order_id_ref = request.GET.get('order_id')
        if request.method == 'POST':
            deleted = request.POST['deleted']
            if deleted == 'deleted':
                payload={}
                ops = request.POST['ops']
                order_id = request.POST['order_id']
                order = OrderProduct.objects.filter(id=order_id, user=request.user, order__order_number=pk, product__slug=ops)
                for item in order:
                    item.cus_item_delete = True
                    item.save()
                payload['response'] = 'success';
                return HttpResponse(json.dumps(payload), content_type="application/json")
            elif deleted == 'refunded':
                order = OrderProduct.objects.filter(id=order_id_ref, user=request.user, order__order_number=pk, product__slug=opsref)
                for item in order:
                    item.cus_ref_accept_del = True
                    item.save()
                messages.success(request, 'Successfully deleted the item.')
                return redirect('dashboard')
    else:
        messages.warning(request, 'Access not permitted!')
        return redirect('store')


# seller use
@login_required(login_url='login')
@allowed_users(allowed_roles=['Seller', 'admin'])
def deleteOrder(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            payload={}
            ops = request.POST['ops']
            order_id = request.POST['order_id']
            order = OrderProduct.objects.filter(id=order_id, order__order_number=pk, product__slug=ops)
            deleted = request.POST['delo']
            if deleted == 'deleted':
                for o in order:
                    o.is_deleted = True
                    o.save()
            elif deleted == 'delete_com':
                for o in order:
                    o.delete()
                payload['response'] = 'success';
            return HttpResponse(json.dumps(payload), content_type="application/json")
    else:
        messages.warning(request, 'Access not permitted!')
        return redirect('store')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def paySeller(request, order_number):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ops = request.POST['ops']
            order_id = request.POST['order_id']
            recieved = request.POST['pay']
            order = OrderProduct.objects.filter(id=order_id, order__order_number=order_number, product__slug=ops)
            if recieved == '12345theone':
                payload={}
                for order in order:
                    order.paid = True
                    order.status = 'PAID'
                    order.for_payment = False
                    order.save()
                    payload['response'] = 'success';
                return HttpResponse(json.dumps(payload), content_type="application/json")
    else:
        messages.warning(request, 'Access not permitted!')
        return redirect('store')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer', 'Seller'])
def item_recieved(request, order_number):
    ops = request.GET.get('ops')
    order = OrderProduct.objects.filter(user=request.user, order__order_number=order_number, product__slug=ops)
    if request.method == 'POST':
        recieved = request.POST['recieved']
        if recieved == '1':
            for order in order:
                order.recieved = True
                if order.request_payment == True:
                    pass
                else:
                    order.for_payment = True
                order.save()
            messages.success(request, 'Thank you for confirming recieved.')
            return redirect('dashboard')
        elif recieved == '2':
            ops_post = request.POST['ops_post']
            payload={}
            cus = request.POST['cus']
            cus_name = Account.objects.get(email=cus)
            order = OrderProduct.objects.filter(user=cus_name, order__order_number=order_number, product__slug=ops_post)
            for item in order:
                item.recieved = True
                if item.for_payment == True:
                    pass
                else:
                    item.request_payment = True
                item.save()
                payload['response'] = 'success';
            return HttpResponse(json.dumps(payload), content_type="application/json")
    else:
        messages.warning(request, 'Access not permitted!')
        return redirect('store')
