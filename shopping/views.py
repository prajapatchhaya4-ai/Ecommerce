from django.shortcuts import render,redirect
from .models import Category,SubCategory, Product
from cart.cart import Cart
from .models import Category, SubCategory, Product
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
# @login_required(login_url="/login/")  

def indexpage(request):
    # Sare categories laa lo
    categories = Category.objects.all()
    category_data = {}

    for category in categories:
        subcategories = SubCategory.objects.filter(category=category)
        subcategory_data = []

        for sub in subcategories:
            products = Product.objects.filter(subcategory=sub)
            subcategory_data.append({
                "subcategory": sub,
                "products": products
            })

        # category name ke hisab se key banao
        category_data[category.name] = subcategory_data

    return render(request, "index.html", {"category_data": category_data,'categories':categories})



# def homepage(request):
#     return render(request,'home.html')

@login_required(login_url="/login/")

def add_to_cart(request,id):
    product = Product.objects.get(id=id)
    cart = Cart(request)
    cart.add(product=product)
    return redirect('/')


def remove_from_cart(request, id):
    product = Product.objects.get(id=id)
    cart = Cart(request)
    cart.remove(product)   
    return redirect('cartdetails')


def increase_quantity(request, id):
    product = Product.objects.get(id=id)
    cart = Cart(request)
    cart.add(product)  # bas quantity badhegi
    return redirect('cartdetails')


def decrease_quantity(request, id):
    product = Product.objects.get(id=id)
    cart = Cart(request)
    cart.decrement(product) 
    return redirect('cartdetails')

# @login_required(login_url="/login/")

def cart_details(request):
    cart = Cart(request)   
    cart_items = cart.cart.values()
    subtotal = sum(float(item['price']) * int(item['quantity']) for item in cart_items)
    tax_per_qty = 20  
    tax = sum(float(item['quantity']) * tax_per_qty for item in cart_items)  
    grand_total = subtotal + tax

    return render(request, "cartdetails.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "tax": tax,
        "grand_total": grand_total
    })

# @login_required(login_url="/login/")
@csrf_exempt
def search(request):
    categories = Category.objects.all()
    query = request.GET.get("q", "").strip()
    products = []
    base_query = query

    if query:
        if query.endswith("s"):  
            base_query = query[:-1]  
        else:  
            base_query = query

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(name__icontains=base_query) |
        Q(subcategory__name__icontains=query) |
        Q(subcategory__name__icontains=base_query) |
        Q(category__name__icontains=query) |
        Q(category__name__icontains=base_query)
        ).distinct()

    return render(request, "search.html", {
        "products": products,
        "query": query,
        'categories':categories
    })
# @login_required(login_url="/login/")
@csrf_exempt
def category_products(request,id):
    category = Category.objects.get(id=id)
    products = Product.objects.filter(category=category)
    return render(request, "search.html", {"category": category,"products": products})

# @login_required(login_url="/login/")
@csrf_exempt
def subcategory_products(request, id):
    # category = Category.objects.get(id=id)
    subcategory = SubCategory.objects.get(id=id)
    products = Product.objects.filter(subcategory=subcategory)

    return render(request, "search.html", {"subcategory": subcategory,"products": products})

# @login_required(login_url="/login/")  
@csrf_exempt  
def product_detail(request, id):
    categories = Category.objects.all()
    product = Product.objects.get(id=id)
    quantity = 1  
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        action = request.POST.get("action")

        if action == "add_to_cart":
            cart = Cart(request)
            cart.add(product=product, quantity=quantity)
            return redirect("cartdetails")
        
    total_price = product.price * quantity

    return render(request, "product_detail.html", {
        "product": product,
        "quantity": quantity,
        "total_price": total_price,
        "categories":categories
    })
    
@login_required(login_url="/login/")
def master(request):
    categories = Category.objects.all()
    return render(request, "master.html", {'categories':categories})

@csrf_exempt
def register_view(request):
    categories = Category.objects.all()
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirmPassword=request.POST['confirmPassword']

        if password != confirmPassword:
            messages.error(request,"Passwords do not match")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,"user already exist") 
            return redirect('signin')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        return redirect('signin')
    return render(request,'register.html',{'categories':categories})

@csrf_exempt
def login_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        username=request.POST['username']
        # email = request.POST['email']
        password=request.POST['password']
        
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        
        else:
            messages.error(request,"Invalid username or password")
            return redirect('signin')
    return render(request,'login.html' ,{'categories':categories})


def logout_view(request):
    logout(request)
    return redirect('/')