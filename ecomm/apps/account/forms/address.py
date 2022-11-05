# from django import forms
# from ecomm.apps.account.models import Address


# class AddressForm(forms.ModelForm):
#     class Meta:
#         model = Address
#         fields = ['full_name', 'phone', 'address_line', 'town_city', 'postcode']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['full_name'].widget.attrs.update(
#             {'class': '', 'placeholder': 'Full Name'}
#         )
#         self.fields['phone'].widget.attrs.update(
#         	{'class': '', 'placeholder': 'Phone'}
#         )
#         self.fields['address_line'].widget.attrs.update(
#             {'class': '', 'placeholder': 'Address'}
#         )
#         self.fields['town_city'].widget.attrs.update(
#             {'class': '', 'placeholder': 'Town/City'}
#         )
#         self.fields['postcode'].widget.attrs.update(
#             {'class': '', 'placeholder': 'Postcode'}
#         )