from django import forms
from .models import Order, OrderProduct

class OrderForm(forms.ModelForm):
    zip  = forms.CharField(min_length=1, max_length=50, help_text='Required')
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'zip', 'currency', 'item_count', 'order_note']

class OrderStatusForm(forms.ModelForm):

    # this is needed if the django vatiabble form is not provided in the html file. using both will duplicate the item
    status = forms.CharField(max_length=25)
    class Meta:
        model = OrderProduct
        fields = ['status']

    def __init__(self, *args, **kwargs): #to override the funtianlity of this particular form
        super(OrderStatusForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['style'] = 'width:200px'
