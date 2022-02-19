from sre_constants import CATEGORY_NOT_SPACE
from unicodedata import category
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render
from core.models import FoodCard, Category, Productscart
from django.contrib.auth import get_user_model

# Create your views here.
def base(request):
    categories = Category.objects.all() 
    foodCards = FoodCard.objects.all()
    context = {'foodCards':foodCards, 'categories':categories}
    return render(request, 'index.html', context=context)


# def test(request, id):
#     categories = Category.objects.all()
#     category = Category.objects.get(id=id)
#     # category1 = FoodCard.objects.all().filter(category=title)
#     print(categories)
#     return render(request, 'index.html', {'categories':categories, 'category':category})

def product(request, id):
    foodcard = FoodCard.objects.get(id=id)
    one_type_categories = FoodCard.objects.all().filter(category=foodcard.category)
    return render(request, 'product.html', {'foodcard':foodcard, 'one_type_categories':one_type_categories})

cart_products = []
rer={}
c = 0
def addCart(request, pk):
    cart_session = request.session.get('cart_session', [])
    print(cart_session)
    cart_products.append(pk)
    products_cart = FoodCard.objects.filter(id__in=cart_products)
    # print(products_cart)
    for i in products_cart:
        p_name=(i.name)
        p_count=(cart_products.count(i.id))
        p_description=(i.description)
        total_sum = cart_products.count(i.id) * i.price
        # print(total_sum)
        # print(i.price)
    context ={'p_name':p_name,'p_count':p_count,'p_description':p_description,'total_sum':total_sum,'':products_cart}    
        


    for i in cart_products:
        if i in rer:
            rer[i] +=1
        else:
            rer[i] = 1
    print(cart_products)
    print('sd',rer[pk])
    product = FoodCard.objects.get(id=pk)
    product_cart = Productscart()
    # product_cart =User
    product_cart.products = product.name
    product_cart.photo = product.image.url
    product_cart.price = product.price
    product_cart.count = rer[pk]
    product_cart.total_sum = product_cart.price  * product_cart.count
    product_cart.save()
    
    
    return HttpResponseRedirect('/')


def cart(request):

    # cart_session = request.session.get('cart_session', [])
    # print(cart_session)
    count_of_product = len(request.session['cart_session'])
        
    # print(count_of_product)
    products_cart = FoodCard.objects.filter(id__in=cart_products)
    # print(products_cart)
    # print(cart_products)
    all_products_sum = 0
    for i in products_cart:

        i.count=cart_products.count(i.id)
        i.sum = cart_products.count(i.id) * i.price
        all_products_sum += i.sum
    context ={'products_cart':products_cart,'all_products_sum':all_products_sum,'count_of_product':count_of_product}   
        


    return render(request, 'cart.html',context=context)

def removecart(request,id):
    cart_session = request.session.get('cart_session', [])
    print(cart_session)
    carts=[]


    for i in cart_session:
        if id != i:
            carts.append(i)
    request.session['cart_session'] = carts
    return redirect ('cart')
    

def about(request):
    return render(request,'about.html')

def search(request):
    if request.method == 'POST':
        search_prod= request.POST.get('search').title()
        # product = FoodCard.objects.get(name=search_prod)
        products =FoodCard.objects.filter(name__contains=search_prod)
        print(search_prod)
        print(product)
        # print(product.price)
    return render (request, 'search.html',{'search_prod':search_prod,'products':products})