from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from Ecomapp.models import *
from django.contrib.auth import aauthenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

from django.shortcuts import render, redirect
from Ecomapp.models import Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from django.contrib.auth.models import User
from Ecomapp.models import Order



def Master(request):
    return render(request , 'master.html')

def Index(request):
    category = Category.objects.all()
    brand = Brand.objects.all() 
    brandID = request.GET.get('brand')
    product = Product.objects.all()
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(Sub_Cateory = categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand = brandID).order_by('-id')
    else:
        product = Product.objects.all()
    
    
    context = {
        'category': category,
        'product':product,
        'brand':brand,
    }
    return render(request , 'index.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Authenticate the user with the username and password1
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],  # Use 'password1' here
            )
            if new_user is not None:  # Ensure the user was successfully authenticated
                login(request, new_user)
                return redirect('index')  # Make sure you have the 'index' view in your urls.py
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'register/signup.html', context)




def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='password_reset_email.html'
            )
            return render(request, 'password_reset_done.html')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset_form.html', {'form': form})

@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    try:
        product = Product.objects.get(id=id)
        cart.add(product=product)
    except Product.DoesNotExist:
        # Handle case where product doesn't exist
        return redirect("index")  # or show an error message
    return redirect("index")


@login_required(login_url="accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return render(request, 'cart/cart_detail.html')



@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product)  # Assuming add() increases quantity
    return render(request, 'cart/cart_detail.html')

@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.decrement(product=product)  # Assuming decrement() decreases quantity
    return render(request, 'cart/cart_detail.html')

@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'cart/cart_detail.html')

@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')



def Contact_page(request):
    if request.method == 'POST':
        contact = Contact_us(
            name= request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )

        contact.save()
    return render (request, 'contact.html')



@login_required
def Checkout(request):
    if request.method == 'POST':
        # Process the order
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart', {})
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk=uid)
        
        for i in cart:
            try:
                a = int(cart[i]['price'])
                b = int(cart[i]['quantity'])
                total = a * b
                order = Order(
                    user=user,
                    product=cart[i]['name'],
                    price=cart[i]['price'],
                    quantity=cart[i]['quantity'],
                    image=cart[i]['image'],
                    address=address,
                    phone=phone,
                    pincode=pincode,
                    total=total,
                )
                order.save()
            except Exception as e:
                print(f"Error processing cart item: {cart[i]} - {e}")
        
        # Clear the cart
        request.session['cart'] = {}
        return redirect('index')
    
    # Render the checkout page if GET request
    cart = request.session.get('cart', {})
    return render(request, 'checkout.html', {'cart': cart})


def Your_order(request):
    uid = request.session.get('_auth_user_id')
    user  = User.objects.get(pk = uid)
    order = Order.objects.filter(user = user)
    print(order)
    context = {
       'order': order,
    }
    return render(request,'order.html',context)
def Product_page(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    product = Product.objects.all()
    categoryID = request.GET.get('category')
    
    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')  # Corrected field name
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all()
    
    context = {
        'category': category,
        'brand': brand,
        'product': product,
    }
    return render(request, 'product.html', context)


def product_detail(request,id):
    product = Product.objects.filter(id = id).first()
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html',context )




def Search(request):
    query = request.GET['query']

    product = Product.objects.filter(name__icontains = query )
    context = {
        'product': product,
    }
    return render(request,'search.html',context)




