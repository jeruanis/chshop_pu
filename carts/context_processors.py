from .models import Cart, CartItem
from .views import _cart_id
from accounts.models import Account
import json
import requests
from urllib.parse import urlparse
from decouple import config
from django.shortcuts import redirect
from django.core.cache import cache

def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)#total user cart_items
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_items = CartItem.objects.all().filter(cart_id=cart[:1])#only need one result
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0

    return dict(cart_count=cart_count)


def country_cur(request):
    # url = request.META.get('HTTP_REFERER') #this is applicable when header gives this META only
    url = request.build_absolute_uri()
    x_forwarded_proto = request.META.get('HTTP_X_FORWARDED_PROTO') #this is applicable when header gives this META only
    ip_add = request.META.get('REMOTE_ADDR')
    if url is not None:
        o = urlparse(url)
        proto = o.scheme
    elif x_forwarded_proto == 'https':
        proto = 'https'
    elif x_forwarded_proto == 'http':
        proto = 'http'
    elif ip_add == '127.0.0.1':
        proto = 'http' #for development local
    else:
        proto = 'https' #always give result when online if those META are not present in the header

    if proto == 'https':
        # two items below produces error
        # ip = requests.get('https://api.ipify.org?format=json')
        # ip_data = json.loads(ip.text) #this is temporary replaced
        # ip_data = ip.json()
        # ip_address = '72.229.28.185' # default to philippines and change only during edit profile
        # ip_address=ip_data['ip'] #this is for production/ this detects the server ip address
        # get ip address
        # req = requests.get('http://ip-api.com/json/' + ip_address+'?fields=country,countryCode,currency')
        req = requests.get('http://ip-api.com/json?fields=country,countryCode,currency')
        dict_result = req.json()
        country = dict_result ['country'] #this depends on the server that the website is using or connected
        country_code = dict_result ['countryCode']
        currency = dict_result ['currency']
    else:
        country = 'Philippines' #if not online
        country_code = 'PH'
        currency = 'PHP'

    logout='logout'
    user = request.user
    user_id = user.id

    if user.is_authenticated: #use this currency if loggedin
        accounts = Account.objects.get(email=user)
        country = accounts.country

    if country == 'Philippines':
        currency='PHP'
        symbol = '₱'
        country_code = 'PH'
    elif country == 'United States':
        currency = 'USD'
        symbol = '$'
        country_code = 'US'
    else:
        country = country
        currency = 'USD'
        symbol = '$'
        country_code = country_code


    return dict(currency=currency, symbol=symbol, country=country, user_id=user_id, logout=logout, protocol=proto)
