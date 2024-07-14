from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Product,Order,OTP,reviews
from django.db.models import Q,Avg,Count
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import random
import hashlib as hash
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
# Create your views here.

def index(request):
    all_products = Product.objects.all()
    count_products=None
    product_ids_list = []
    category_list=[]

    for i in all_products:
        if i.category_1 not in category_list and i.category_1!="" and i.category_1!="all":
            category_list.append(i.category_1)
        if i.category_2 not in category_list and i.category_2!="" and i.category_2!="all":
            category_list.append(i.category_2)
        if i.category_3 not in category_list and i.category_3!="" and i.category_3!="all":
            category_list.append(i.category_3)
        if i.category_4 not in category_list and i.category_4!="" and i.category_4!="all":
            category_list.append(i.category_4)
        if i.category_5 not in category_list and i.category_5!="" and i.category_5!="all":
            category_list.append(i.category_5)

    # Get the order for the current user that hasn't been placed yet
    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        order_ids=order_items.product_id.split(",")
        for i in order_ids:
            product_ids_list.append(int(i))
    except:
        pass
    
    # code for searching
    search_var=None
    item_name=request.POST.get("item_name")
    if item_name!='' and item_name is not None:
        all_products=all_products.filter(name__icontains=item_name)
        search_var=item_name

    category=request.GET.get("category")
    if category!="all" and category is not None:
        all_products=all_products.filter(Q(category_1=category) | Q(category_2=category) | Q(category_3=category) | Q(category_4=category) | Q(category_5=category))

    # code for pagination
    paginator=Paginator(all_products,32) # 32 products per page
    page=request.GET.get("page")
    all_products=paginator.get_page(page)

    if len(product_ids_list)>0:
        count_products=len(product_ids_list)



    # code for getting cart products
    try:

        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        int_ids=[]
        int_price=[]
        int_quantity=[]

        total_ind_price=[]

        for i in range(len(str_ids)):
            int_ids.append(int(str_ids[i]))
            int_price.append(int(str_price[i]))
            int_quantity.append(int(str_quantity[i]))

            total_ind_price.append(int(str_price[i])*int(str_quantity[i]))

        gross_total=sum(total_ind_price)

        d={
            "ids":int_ids,
            "quantity":int_quantity,
            "price":total_ind_price,
        }

        zipped_data=zip(d["ids"],d["quantity"],d["price"])

    except:
        order_items=None
        zipped_data=None
        gross_total=None


    context = {
        "all_products": all_products,
        "product_ids_list": product_ids_list,
        "count_products":count_products,
        "gross_total":gross_total,
        "category_list":category_list,
        "search_var":search_var,
        "cart_products":zipped_data if zipped_data else None
    }

    return render(request, "index.html", context)

def details(request, id):
    all_products=Product.objects.all()
    product = get_object_or_404(Product, id=id)
    count_products=None
    product_ids_list = []

    
    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        order_ids=order_items.product_id.split(",")
        for i in order_ids:
            product_ids_list.append(int(i))
    except:
        pass

    if len(product_ids_list)>0:
        count_products=len(product_ids_list)

    description_list=product.description.split("\n")

    # code for getting related category products
    category_products=all_products.filter(Q(category_1=product.category_1) | Q(category_2=product.category_1) | Q(category_3=product.category_1) | Q(category_4=product.category_1) | Q(category_5=product.category_1))

    # code for getting cart products
    try:

        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        int_ids=[]
        int_price=[]
        int_quantity=[]

        total_ind_price=[]

        for i in range(len(str_ids)):
            int_ids.append(int(str_ids[i]))
            int_price.append(int(str_price[i]))
            int_quantity.append(int(str_quantity[i]))

            total_ind_price.append(int(str_price[i])*int(str_quantity[i]))

        gross_total=sum(total_ind_price)

        d={
            "ids":int_ids,
            "quantity":int_quantity,
            "price":total_ind_price,
        }

        zipped_data=zip(d["ids"],d["quantity"],d["price"])

    except:
        order_items=None
        zipped_data=None
        gross_total=None

    if request.method=="POST":
        rating=int(request.POST.get("rating","1"))
        name=request.POST.get("name")
        email=request.POST.get("email")
        message=request.POST.get("message")

        product_instance=get_object_or_404(Product,id=id)
        obj=reviews.objects.create(product=product_instance,rating=rating,name=name,email=email,review=message)
        obj.save()

    review_instance=None
    product_instance=get_object_or_404(Product,id=id)
    review_instance=reviews.objects.filter(product=product_instance)

    average_rating=review_instance.aggregate(Avg("rating"))["rating__avg"]
    rating_count=review_instance.aggregate(Count("rating"))["rating__count"]

    context = {
        "all_products":all_products,
        "category_products":category_products,
        "product": product,
        "product_ids_list": product_ids_list,
        "count_products":count_products,
        "description_list":description_list,
        "gross_total":gross_total,
        "cart_products":zipped_data if zipped_data else None,
        "review_instance":review_instance,
        "one":[1],
        "two":[2],
        "three":[3],
        "four":[4],
        "five":[5],
        "average_rating":round(average_rating,1),
        "rating_count":rating_count
    }
    return render(request, "details.html", context)


from django.http import JsonResponse

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    response_data = {'success': False}

    try:
        order_items = get_object_or_404(Order, user=request.user, order_placed=False)
        str_ids = order_items.product_id.split(",")
        str_name = order_items.product_name.split(",")
        str_price = order_items.product_price.split(",")
        str_quantity = order_items.product_quantity.split(",")

        str_ids.append(str(product.id))
        str_name.append(product.name)
        str_price.append(str(product.price))
        str_quantity.append("1")

        order_items.product_id = ",".join(str_ids)
        order_items.product_name = ",".join(str_name)
        order_items.product_price = ",".join(str_price)
        order_items.product_quantity = ",".join(str_quantity)
        order_items.save()

    except:
        order_items = Order.objects.create(
            user=request.user,
            product_name=product.name,
            product_id=str(product.id),
            product_price=product.price,
            product_quantity="1"
        )
        order_items.save()

    response_data['success'] = True
    response_data['action'] = 'add'
    response_data['product_id'] = product.id

    if is_ajax(request):
        return JsonResponse(response_data)
    else:
        return redirect("index")

@login_required
def remove_from_cart(request, id):
    product = get_object_or_404(Product, id=id)
    response_data = {'success': False}

    try:
        order_items = get_object_or_404(Order, user=request.user, order_placed=False)
        str_ids = order_items.product_id.split(",")
        str_name = order_items.product_name.split(",")
        str_price = order_items.product_price.split(",")
        str_quantity = order_items.product_quantity.split(",")

        index_id = str_ids.index(str(product.id))

        str_ids.pop(index_id)
        str_name.pop(index_id)
        str_price.pop(index_id)
        str_quantity.pop(index_id)

        if len(str_ids) > 0:
            order_items.product_id = ",".join(str_ids)
            order_items.product_name = ",".join(str_name)
            order_items.product_price = ",".join(str_price)
            order_items.product_quantity = ",".join(str_quantity)
            order_items.save()
        else:
            order_items.delete()

    except:
        pass

    response_data['success'] = True
    response_data['action'] = 'remove'
    response_data['product_id'] = product.id

    if is_ajax(request):
        return JsonResponse(response_data)
    else:
        return redirect("index")
    

@login_required
def update_cart(request,id):
    update_quantity=str(request.POST.get('quantity', 1))
    order_items=get_object_or_404(Order,user=request.user,order_placed=False)
    str_ids=order_items.product_id.split(",")
    str_quantity=order_items.product_quantity.split(",")

    ind=str_ids.index(str(id))
    str_quantity[ind]=update_quantity

    order_items.product_quantity=",".join(str_quantity)
    order_items.save()

    return redirect("details", id=id)


@login_required
def update_cart_redirect_cart(request,id):
    update_quantity=str(request.POST.get('quantity', 1))
    order_items=get_object_or_404(Order,user=request.user,order_placed=False)
    str_ids=order_items.product_id.split(",")
    str_quantity=order_items.product_quantity.split(",")

    ind=str_ids.index(str(id))
    str_quantity[ind]=update_quantity

    order_items.product_quantity=",".join(str_quantity)
    order_items.save()

    return redirect("cart")



@login_required
def add_to_cart_product_redirect(request, id):
    product = get_object_or_404(Product, id=id)

    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        str_ids.append(str(product.id))
        str_name.append(product.name)
        str_price.append(str(product.price))

        update_quantity=str(request.POST.get('quantity', 1))
        str_quantity.append(update_quantity)

        order_items.product_id=",".join(str_ids)
        order_items.product_name=",".join(str_name)
        order_items.product_price=",".join(str_price)
        order_items.product_quantity=",".join(str_quantity)
        order_items.save()

    except:
        order_items=Order.objects.create(
            user=request.user,
            product_name=product.name,
            product_id=str(product.id),
            product_price=product.price,
            product_quantity=str(request.POST.get('quantity', 1))
        )
        order_items.save()

    return redirect("details", id=id)


@login_required
def remove_from_cart_product_redirect(request, id):
    product = get_object_or_404(Product, id=id)

    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        index_id=str_ids.index(str(product.id))

        str_ids.pop(index_id)
        str_name.pop(index_id)
        str_price.pop(index_id)
        str_quantity.pop(index_id)

        if len(str_ids)>0:
            order_items.product_id=",".join(str_ids)
            order_items.product_name=",".join(str_name)
            order_items.product_price=",".join(str_price)
            order_items.product_quantity=",".join(str_quantity)
            order_items.save()
        else:
            order_items.delete()

    except:
        pass

    return redirect("details", id=id)


@login_required
def remove_from_cart_redirect_cart(request,id):
    product = get_object_or_404(Product, id=id)

    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        index_id=str_ids.index(str(product.id))

        str_ids.pop(index_id)
        str_name.pop(index_id)
        str_price.pop(index_id)
        str_quantity.pop(index_id)

        if len(str_ids)>0:
            order_items.product_id=",".join(str_ids)
            order_items.product_name=",".join(str_name)
            order_items.product_price=",".join(str_price)
            order_items.product_quantity=",".join(str_quantity)
            order_items.save()
        else:
            order_items.delete()

    except:
        pass


    return redirect("cart")




@login_required
def cart(request):
    all_products=Product.objects.all()
    count_products=None
    product_ids_list=[]

    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        for i in str_ids:
            product_ids_list.append(int(i))

        int_ids=[]
        int_price=[]
        int_quantity=[]

        total_ind_price=[]

        for i in range(len(str_ids)):
            int_ids.append(int(str_ids[i]))
            int_price.append(int(str_price[i]))
            int_quantity.append(int(str_quantity[i]))
            total_ind_price.append(int(str_price[i])*int(str_quantity[i]))

        if len(int_ids)>0:
            count_products=len(int_ids)

        gross_total=sum(total_ind_price)
        shipping=200
        shipped_total=gross_total+shipping

        you_save=[]
        gross_without_discount_list=[]
        for prod in all_products:
            if prod.id in int_ids:
                if prod.price_without_discount:
                    indexed=int_ids.index(prod.id)
                    gross_without_discount_list.append(prod.price_without_discount*int_quantity[indexed])
                    you_save.append((prod.price_without_discount-prod.price)*int_quantity[indexed])
                else:
                    indexed=int_ids.index(prod.id)
                    gross_without_discount_list.append(prod.price*int_quantity[indexed])

        gross_without_discount=sum(gross_without_discount_list)
        total_you_save=sum(you_save)


        d={
            "ids":int_ids,
            "quantity":int_quantity,
            "price":int_price,
            "total_ind_price":total_ind_price,
        }

        zipped_data=zip(d["ids"],d["quantity"],d["price"],d["total_ind_price"])
        zip_new=zipped_data

    except:
        order_items=None
        zipped_data=None
        gross_total=0
        total_you_save=0
        shipped_total=0
        shipping=0
        gross_without_discount=0
        zip_new=None

    context={
        "all_products":all_products,
        "count_products":count_products,
        "gross_total":gross_total,
        "cart_products":zipped_data if zipped_data else None,
        "zip_new":zip_new,
        "product_ids_list":product_ids_list,
        "total_you_save":total_you_save,
        "shipped_total":shipped_total,
        "shipping":shipping,
        "gross_without_discount":gross_without_discount
    }

    
    return render(request, 'cart.html', context)

@login_required
def delivery_details(request):
    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        if request.method=="POST":
            phone=request.POST.get("phone")
            address=request.POST.get("address")
            order_items.phone=phone
            order_items.address=address
            order_items.email=request.user.email
            order_items.order_date=timezone.now()
            order_items.save()

            return redirect("order_summary")
    except:
        order_items=None
    return render(request,"delivery_details.html")


@login_required
def order_summary(request):
    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        int_ids=[]
        int_price=[]
        int_quantity=[]

        total_ind_price=[]

        for i in range(len(str_ids)):
            int_ids.append(int(str_ids[i]))
            int_price.append(int(str_price[i]))
            int_quantity.append(int(str_quantity[i]))
            total_ind_price.append(int(str_price[i])*int(str_quantity[i]))

        subtotal=sum(total_ind_price)
        gross_total=subtotal+200

        

        d={
            "ids":int_ids,
            "name":str_name,
            "price":int_price,
            "total_price":total_ind_price,
            "quantity":int_quantity
        }

        zipped_data=zip(d["ids"],d["name"],d["price"],d["total_price"],d["quantity"])

        first_name=request.user.first_name
        last_name=request.user.last_name
        email=order_items.email
        phone=order_items.phone
        address=order_items.address
        order_id=f"ODRNO007N{order_items.id}"
        date=order_items.order_date
    except:
        order_items=None
        zipped_data=None
        first_name=None
        last_name=None
        email=None
        phone=None
        address=None
        order_id=None
        date=None
        subtotal=None
        gross_total=None

    context={
        "zipped_data":zipped_data,
        "first_name":first_name,
        "last_name":last_name,
        "email":email,
        "phone":phone,
        "address":address,
        "order_id":order_id,
        "date":date,
        "subtotal":subtotal,
        "gross_total":gross_total
    }

    if zipped_data:
        subject="Your Order Summary"
        html_content=render_to_string("order_summary.html",context)
        text_data=strip_tags(html_content)
        from_email=settings.EMAIL_HOST_USER
        to_email=email

        email = EmailMultiAlternatives(subject, text_data, from_email=from_email, to=[to_email,"mianjunaidoffical@gmail.com"])
        email.attach_alternative(html_content,"text/html")
        email.send()

    return redirect("order_summary_new")

@login_required
def order_summary_new(request):
    all_products=Product.objects.all()
    count_products=None
    product_ids_list=[]

    try:
        order_items=get_object_or_404(Order,user=request.user,order_placed=False)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        for i in str_ids:
            product_ids_list.append(int(i))

        int_ids=[]
        int_price=[]
        int_quantity=[]

        total_ind_price=[]

        for i in range(len(str_ids)):
            int_ids.append(int(str_ids[i]))
            int_price.append(int(str_price[i]))
            int_quantity.append(int(str_quantity[i]))
            total_ind_price.append(int(str_price[i])*int(str_quantity[i]))

        if len(int_ids)>0:
            count_products=len(int_ids)

        gross_total=sum(total_ind_price)
        shipping=200
        shipped_total=gross_total+shipping

        you_save=[]
        gross_without_discount_list=[]
        for prod in all_products:
            if prod.id in int_ids:
                if prod.price_without_discount:
                    indexed=int_ids.index(prod.id)
                    gross_without_discount_list.append(prod.price_without_discount*int_quantity[indexed])
                    you_save.append((prod.price_without_discount-prod.price)*int_quantity[indexed])
                else:
                    indexed=int_ids.index(prod.id)
                    gross_without_discount_list.append(prod.price*int_quantity[indexed])

        gross_without_discount=sum(gross_without_discount_list)
        total_you_save=sum(you_save)


        d={
            "ids":int_ids,
            "quantity":int_quantity,
            "price":int_price,
            "total_ind_price":total_ind_price,
        }

        zipped_data=zip(d["ids"],d["quantity"],d["price"],d["total_ind_price"])
        zip_new=zipped_data

        order_id=f"ORDNO007N{order_items.id}"
        name=f"{request.user.first_name} {request.user.last_name}"
        email=order_items.email
        phone=order_items.phone
        address=order_items.address
        date=order_items.order_date

        order_items.order_placed=True
        order_items.save()

    except:
        order_items=None
        zipped_data=None
        gross_total=0
        total_you_save=0
        shipped_total=0
        shipping=0
        gross_without_discount=0
        zip_new=None
        order_id=None
        name=None
        email=None
        phone=None
        address=None
        date=None

    context={
        "all_products":all_products,
        "count_products":count_products,
        "gross_total":gross_total,
        "cart_products":zipped_data if zipped_data else None,
        "zip_new":zip_new,
        "product_ids_list":product_ids_list,
        "total_you_save":total_you_save,
        "shipped_total":shipped_total,
        "shipping":shipping,
        "gross_without_discount":gross_without_discount,
        "order_id":order_id,
        "name":name,
        "email":email,
        "phone":phone,
        "address":address,
        "date":date
    }

    return render(request,"order_summary_new.html",context)

@login_required
def all_prev_orders(request):
    order_objects=Order.objects.filter(user=request.user,order_placed=True)
    context={
        "order_objects":order_objects,
    }
    return render(request,"all_prev_orders.html",context)

@login_required
def one_prev_order(request,id):
    
    all_products=Product.objects.all()
    count_products=None
    product_ids_list=[]

    try:
        order_items=get_object_or_404(Order,id=id,user=request.user,order_placed=True)
        str_ids=order_items.product_id.split(",")
        str_name=order_items.product_name.split(",")
        str_price=order_items.product_price.split(",")
        str_quantity=order_items.product_quantity.split(",")

        for i in str_ids:
            product_ids_list.append(int(i))

        int_ids=[]
        int_price=[]
        int_quantity=[]

        total_ind_price=[]

        for i in range(len(str_ids)):
            int_ids.append(int(str_ids[i]))
            int_price.append(int(str_price[i]))
            int_quantity.append(int(str_quantity[i]))
            total_ind_price.append(int(str_price[i])*int(str_quantity[i]))

        if len(int_ids)>0:
            count_products=len(int_ids)

        gross_total=sum(total_ind_price)
        shipping=200
        shipped_total=gross_total+shipping

        you_save=[]
        gross_without_discount_list=[]
        for prod in all_products:
            if prod.id in int_ids:
                if prod.price_without_discount:
                    indexed=int_ids.index(prod.id)
                    gross_without_discount_list.append(prod.price_without_discount*int_quantity[indexed])
                    you_save.append((prod.price_without_discount-prod.price)*int_quantity[indexed])
                else:
                    indexed=int_ids.index(prod.id)
                    gross_without_discount_list.append(prod.price*int_quantity[indexed])

        gross_without_discount=sum(gross_without_discount_list)
        total_you_save=sum(you_save)


        d={
            "ids":int_ids,
            "quantity":int_quantity,
            "price":int_price,
            "total_ind_price":total_ind_price,
        }

        zipped_data=zip(d["ids"],d["quantity"],d["price"],d["total_ind_price"])
        zip_new=zipped_data

        order_id=f"ORDNO007N{order_items.id}"
        name=f"{request.user.first_name} {request.user.last_name}"
        email=order_items.email
        phone=order_items.phone
        address=order_items.address
        date=order_items.order_date

        order_items.order_placed=True
        order_items.save()

    except:
        order_items=None
        zipped_data=None
        gross_total=0
        total_you_save=0
        shipped_total=0
        shipping=0
        gross_without_discount=0
        zip_new=None
        order_id=None
        name=None
        email=None
        phone=None
        address=None
        date=None

    context={
        "all_products":all_products,
        "count_products":count_products,
        "gross_total":gross_total,
        "cart_products":zipped_data if zipped_data else None,
        "zip_new":zip_new,
        "product_ids_list":product_ids_list,
        "total_you_save":total_you_save,
        "shipped_total":shipped_total,
        "shipping":shipping,
        "gross_without_discount":gross_without_discount,
        "order_id":order_id,
        "name":name,
        "email":email,
        "phone":phone,
        "address":address,
        "date":date
    }

    return render(request,"order_summary_new.html",context)



def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            # Send email confirmation
            otp = str(random.randint(100000, 999999))

            sha256hash=hash.sha256()
            sha256hash.update(otp.encode("utf-8"))
            otp_hash=sha256hash.hexdigest()


            user_obj = get_object_or_404(User, username=form.cleaned_data.get("email"))
            instance = OTP.objects.create(user=user_obj, otp=otp_hash)
            instance.save()
            
            # Sending Mail with otp
            mail_subject = 'Activate your account'
            message = f"{otp}"
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject,message,settings.EMAIL_HOST_USER,[to_email])
            email.send()
            
            return redirect('registration_confirmation')
    else:
        form = CustomUserCreationForm()
    

    return render(request, 'register_user.html', {'form': form})

# First, delete expired OTPs and associated user accounts
expired_records = OTP.objects.filter(timestamp__lte=timezone.now() - timedelta(minutes=30))
for record in expired_records:
    user = record.user
    user.delete()

expired_records.delete()

def registration_confirmation(request):
    # First, delete expired OTPs and associated user accounts
    expired_records = OTP.objects.filter(timestamp__lte=timezone.now() - timedelta(minutes=30))
    for record in expired_records:
        user = record.user
        user.delete()

    expired_records.delete()

    user_obj = None
    if request.method == "POST":
        otp = request.POST.get("otp")

        sha256hash=hash.sha256()
        sha256hash.update(otp.encode("utf-8"))
        otp_hash=sha256hash.hexdigest()

        
        try:
            otp_obj = get_object_or_404(OTP, otp=otp_hash)
            user_id = otp_obj.user_id
            user_obj = get_object_or_404(User, id=user_id)
            
            
            user_obj.is_active = True
            user_obj.save()
            otp_obj.delete()
        except:
            return redirect("otp_failed")
    
    context = {"user_obj": user_obj}

    return render(request, 'registration_confirmation.html', context)

def otp_failed(request):
    return render(request,"otp_failed.html")

def login_user(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect("index")
    else:
        form=AuthenticationForm()
    context={"form":form}
    return render(request,"login_user.html",context)


def about(request):
    return render(request,"about-us.html")

def logout_user(request):
    logout(request)
    return redirect("login_user")