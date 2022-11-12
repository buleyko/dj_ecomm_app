from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import ( 
	get_object_or_404, 
	render,
	redirect,
)
from ecomm.apps.account.models import (
	Account,
	Address,
)
from ecomm.apps.account.forms.address import AddressForm



@login_required
@require_http_methods(['GET'])
def index(request):
    addresses = Address.objs.filter(account=request.user).order_by('-default')
    return render(request, 'apps/account/address/list.html', {
        'addresses': addresses
    })


# @login_required
# @require_http_methods(['GET'])
# def create(request):
#     form = AddressForm()
#     return render(request, 'apps/account/address/create.html', {
#         'form': form
#     })


# @login_required
# @require_http_methods(['POST'])
# def store(request):
#     form = AddressForm(request.POST)
#     if form.is_valid():
#         form = form.save(commit=False)
#         form.account = request.user
#         form.save()
#         return redirect('account:address_list')
#     else:
#         form = AddressForm(data=request.POST)
#         return render(request, 'apps/account/address/create.html', {
#             'form': form
#         })


@login_required
@require_http_methods(['GET'])
def edit(request, pk):
    # address = Address.objs.get(pk=pk, account=request.user)
    address = get_object_or_404(Address, pk=pk, account=request.user)
    form = AddressForm(instance=address)
    return render(request, 'apps/account/address/edit.html', {
        'form': form
    })


@login_required
@require_http_methods(['POST'])
def update(request):
    pk = request.POST['id']
    # address = Address.objs.get(pk=pk, account=request.user)
    address = get_object_or_404(Address, pk=pk, account=request.user)
    form = AddressForm(instance=address, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('account:address_list')
    else:
        form = AddressForm(data=request.POST)
        return render(request, 'apps/account/address/edit.html', {
            'form': form
        })


@login_required
@require_http_methods(['GET'])
def destroy(request, pk):
    address = Address.objs.filter(pk=pk, account=request.user).\
        delete()
    return redirect('account:address_list')


@login_required
@require_http_methods(['GET'])
def set_default(request, pk):
    Address.objs.filter(account=request.user, default=True).\
        update(default=False)
    Address.objs.filter(pk=pk, account=request.user).\
        update(default=True)
    # previous_url = request.META.get('HTTP_REFERER')
    # if 'delivery_address' in previous_url:
    #     return redirect('checkout:delivery_address')
    return redirect('account:address_list')


