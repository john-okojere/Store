from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail

def homepage(request):
    products = Product.objects.all().order_by('-created_date')
    return render(request, 'home/index.html', {'products':products})

def FAQ(request):
    return render(request, 'home/faq.html')

def about(request):
    return render(request, 'home/about.html')

def returnPolicy(request):
    return render(request, 'home/returnPolicy.html')

def TermsCondition(request):
    return render(request, 'home/TermsCondition.html')


def privacyPolicy(request):
    return render(request, 'home/PrivacyPolicy.html')

def deliveryPolicy(request):
    return render(request, 'home/delivery.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        subject = 'Message from LOT Store Contact Form'
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        recipient_email = 'johnokojere08@gmail.com'

        try:
            send_mail(subject, body, email, [recipient_email])
            return JsonResponse({'success': True, 'message': 'Email sent successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return render(request, 'home/contact.html')

def category_view(request, cat):
    cate = Category.objects.get(name = cat)
    products = Product.objects.filter(categories=cate).order_by('-created_date')
    info = f'Result for {cate.name} items'
    return render(request, 'home/index.html', {'products':products, 'info':info})


def details(request, uid):
    product = Product.objects.get(uid=uid)
    products = Product.objects.all().order_by('-created_date')
    return render(request, 'home/details.html', {'product':product,'products':products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            form.save()
            return redirect('/')
    else:
        form = ProductForm()
    
    return render(request, 'home/add_product.html', {'form': form})

@login_required
def edit_product(request, uid):
    product  = Product.objects.get(uid = uid)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            form.save()
            return redirect('/')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'home/add_product.html', {'form': form})


def filter_items(request):
    if request.method == 'POST':
        category_id = request.POST.get('category-filter')
        size_filter = request.POST.getlist('size')
        min_price_filter = request.POST.get('min-price')
        max_price_filter = request.POST.get('max-price')

        queryset = Product.objects.all()

        if category_id != '0':
            queryset = queryset.filter(categories__id=category_id)

        if size_filter:
            size_q_objects = Q()
            for size in size_filter:
                size_q_objects |= Q(size=size)
            queryset = queryset.filter(size_q_objects)

        if min_price_filter:
            queryset = queryset.filter(price__gte=min_price_filter)
        else:
            queryset = queryset.filter(price__gte=0)

        if max_price_filter:
            queryset = queryset.filter(price__lte=max_price_filter)
        else:
            queryset = queryset.filter(price__lte=10000)

        info = f"Filter result: {len(queryset)}"
        context ={
                'products': queryset, 
                'info':info,
                'category_id':category_id,
                'size_filter':size_filter,
                'min_price_filter':min_price_filter,
                'max_price_filter':max_price_filter,
            }
        return render(request, 'home/index.html', context)

    return render(request, 'home/index.html')  



def search(request):
    search = request.GET.get('item')
    print(search)
    if search:
        filtered_items = Product.objects.filter(
            Q(name__icontains=search) | 
            Q(categories__name__icontains=search) | 
            Q(size__icontains=search) | 
            Q(description__icontains=search)
        )
        info = f"Search result for {search}: {len(filtered_items)}"
    else:
        filtered_items =  Product.objects.all()
        info = f"Search result for {search} not found"
    return render(request, 'home/index.html', {'products':filtered_items, 'info':info}) 

def search_suggestions(request):
    if 'item' in request.GET:
        search_term = request.GET['item']
        suggestions = Product.objects.filter(name__icontains=search_term)[:5]
        suggestions_data = []
        for product in suggestions:
            product_data = {
                'name': product.name,
                'size': product.size,
                'price': product.price,
                'image': product.image.url,  # Assuming image field is a FileField or ImageField
                'details_url': product.uid # Assuming you have a method to get product details URL
            }
            suggestions_data.append(product_data)
        return JsonResponse({'suggestions': suggestions_data})
    return JsonResponse({})