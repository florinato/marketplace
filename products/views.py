from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

from chat.models import Conversation
from products.forms import ProductForm, ReportForm  # Import ReportForm
from products.models import Product, Report  # Import Report model


def product_list(request):
    products = Product.objects.filter(is_withdrawn=False, is_sold=False, is_blocked=False)
    return render(request, 'products/product_list.html', {'products': products})

from products.models import ProductImage


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    images = ProductImage.objects.filter(product=product)
    return render(request, 'products/product_detail.html', {'product': product, 'images': images})


def get_products_api(request):
    products = Product.objects.all()
    product_list = []
    for product in products:
        product_list.append({
            'pk': product.pk,
            'title': product.title,
            'price': str(product.price),
            'user': product.user.username,
            'main_image': settings.MEDIA_URL + str(product.main_image) if product.main_image else None,
        })
    return JsonResponse({"products": product_list}, safe=False)

def report_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report = Report(
                reported_user=product.user,
                product=product,
                reporter=request.user,
                reason=report_form.cleaned_data['reason']
            )
            report.save()
            return redirect('products:product_detail', pk=product_id) # Redirect to product detail after report
    else:
        report_form = ReportForm()
    return render(request, 'reports/report_product.html', {'product': product, 'form': report_form}) # Pass the form to the template


def mark_as_sold_or_withdraw(request, pk):
    product = Product.objects.get(pk=pk)
    users_with_chat_ids = Conversation.objects.filter(product=product).values_list('participants__id', flat=True).distinct()
    users_with_chat_list = []
    for user_id in users_with_chat_ids:
        users_with_chat_list.append(User.objects.get(pk=user_id))

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'withdraw':
            product.is_withdrawn = True
        elif action == 'sell':
            buyer_id = request.POST.get('buyer')
            if buyer_id:
                product.is_sold = True
                product.buyer_id = buyer_id
        product.save()
        return render(request, 'products/product_detail.html', {'product': product, 'users_with_chat_list': users_with_chat_list})
