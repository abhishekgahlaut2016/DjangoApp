from django.shortcuts import render
from .models import Question, Register, ProductImage, ProductCategory, BuyerDetail, Cart
from django.template import loader
from django import forms
import paypalrestsdk
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime,timedelta
from django.db import connection



# Create your views here.

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

def index(request):
    context = {}
    list1 = []
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    get_records = ProductImage.objects.all()
    if get_records:
        for val in get_records:
            image_prod = str(val.product_image).split('polls',1)[1]
            list1.append(image_prod)
        context = {'latest_question_list': latest_question_list, 'all_images':list1}
    else:
        pass  
    return render(request, 'polls/index.html', context)


def image_detail(request):
    context = {}
    email = ''
    
    no_of_cart_items = request.session.get('no_of_cart_items',0)
    user_id = request.session.get('user_id')
    get_user = Register.objects.filter(id=user_id)
    if get_user:
      email = get_user[0].email

    image_name = request.GET.get('image_name','')
    tot_img_path = 'polls'+str(image_name)
    prod_search = ProductImage.objects.filter(product_image=tot_img_path)
    if prod_search:
        prod_id = prod_search[0].id
        prod_name = prod_search[0].name
        prod_desc = prod_search[0].description
        prod_manufacturer = prod_search[0].manufacturer
        prod_price = prod_search[0].price_in_dollars
        context = {'image_name':image_name,'prod_name':prod_name,'prod_desc':prod_desc,'prod_manufacturer':prod_manufacturer,'prod_price':prod_price,'prod_id':prod_id,'login_email':email,'no_of_cart_items':no_of_cart_items}

      
    return render(request, 'polls/image_detail.html', context)    

def register(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/register.html', {})    


class register_user_form(forms.ModelForm):
    class Meta:
        model = Register
        fields = ('email', 'password','mobile')
     
def register_user(request):
    if request.POST:
        field1_value = request.POST.get('signup_email','')
        field2_value = request.POST.get('signup_mobile','')
        field3_value = request.POST.get('signup_password','')
        field4_value = request.POST.get('signup_confirm_password','')
        instance = Register(email=field1_value,mobile=field2_value,password=field3_value)
        instance.save()
    return render(request, 'polls/index.html')


def login(request):
    email = ''
    list1 = []
    context = {}

    get_products = ProductImage.objects.all()
    if get_products:
        for val in get_products:
            image_prod = str(val.product_image).split('polls',1)[1]
            list1.append(image_prod)
        context = {'all_images':list1}

    field1_value = request.POST.get('login_email','')
    field2_value = request.POST.get('login_password','')
    get_records = Register.objects.filter(email=field1_value,password=field2_value)
    if get_records:
        request.session.set_expiry(0)
        request.session['user_id'] = get_records[0].id
        email = get_records[0].email

        ### Get all cart items for current user
        get_cart_items = Cart.objects.filter(register_id=get_records[0].id)
        if get_cart_items:
          no_of_cart_items = len(get_cart_items)
          request.session['no_of_cart_items'] = no_of_cart_items

        context.update({'login_email':email})
        return render(request, 'polls/index.html', context)

    return HttpResponse('Invalid Email / Password')


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponse("Logged Out")    


class cart_form(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('product_id', 'price', 'quantity', 'register_id') 

def add_to_cart(request):
    product_id = False
    price = 0.00

    user_id = request.session.get('user_id',False)
    if user_id:
      user_id = int(user_id)
      user_id = Register.objects.get(id=user_id)

    prod_id = request.GET.get('prod_id',False)
    if prod_id:
      prod_id = int(prod_id)
      product_id = ProductImage.objects.get(id=prod_id)

    price = request.GET.get('price',0.00)
    if price:
      price = float(price)

    quantity = 1.0

    instance = Cart(product_id=product_id, price=price, quantity=quantity, register_id=user_id)
    instance.save()

    ### Update Cart Items
    if user_id:
        get_cart_items = Cart.objects.filter(register_id=user_id)
        if get_cart_items:
          no_of_cart_items = len(get_cart_items)
          request.session['no_of_cart_items'] = no_of_cart_items

    return HttpResponse('')


def buy_product(request):
    return render(request, 'polls/buy.html', {})

def cart_items(request):
    ##### When Remove Item From Cart
    if request.GET:
        cart_id = request.GET.get('cart_id',False)
        if cart_id:
            cart_id = int(cart_id)
            cart_id = Cart.objects.get(id=cart_id)
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM polls_cart WHERE id=%s",[cart_id.id])
    ##########            

    context = {}
    no_of_cart_items = 0
    price_subtotal = 0
    estimated_shipping_cost = 5
    user_id = request.session.get('user_id',False)
    if user_id:
        user_id = int(user_id)
        user_id = Register.objects.get(id=user_id)

        get_cart_items = Cart.objects.filter(register_id=user_id)
        if get_cart_items:
            for val in get_cart_items:
                price_subtotal = price_subtotal + val.price
            price_total = estimated_shipping_cost + price_subtotal    
            context.update({'all_items':get_cart_items,'price_subtotal':price_subtotal,'estimated_shipping_cost':estimated_shipping_cost,'price_total':price_total})

        if get_cart_items: 
            no_of_cart_items = len(get_cart_items)
        request.session['no_of_cart_items'] = no_of_cart_items      

    return render(request, 'polls/cart_items.html', context) 



class buyer_detail_form(forms.ModelForm):
    class Meta:
        model = BuyerDetail
        fields = ('buyer_name', 'buyer_email','buyer_mobile','buyer_address1','buyer_address2','buyer_pincode','buyer_city','buyer_state','buyer_country')    

def make_payment(request):
    if request.POST:
       field1_value = request.POST.get('fullname','')
       field2_value = request.POST.get('buy_email','')
       field3_value = request.POST.get('buy_mobile','')
       field4_value = request.POST.get('buy_address1','')
       field5_value = request.POST.get('buy_address2','')
       field6_value = request.POST.get('buy_pincode','')
       field7_value = request.POST.get('buy_city','')
       field8_value = request.POST.get('buy_state','')
       field9_value = request.POST.get('country','')

       instance = BuyerDetail(buyer_name=field1_value, buyer_email=field2_value, buyer_mobile=field3_value, buyer_address1=field4_value, buyer_address2=field5_value, buyer_pincode=field6_value, buyer_city=field7_value, buyer_state=field8_value, buyer_country=field9_value)
       instance.save()

    return render(request, 'polls/payment.html', {})    



def paypal_process(request):
    status = ''
    transaction_id = ''
    current_date = datetime.now()
    payment_json = ''
    #mainLayout = MainLayout()
   # config = get_config()
    state = 'Payment Successful'
    alldata = request.POST
    if request.POST:
      contact_first_name = alldata.get('contact_first_name','')
      contact_last_name = alldata.get('contact_last_name','')
      contact_email = alldata.get('contact_email','')
      contact_mobile = alldata.get('contact_mobile','')
      card_holder_first_name = alldata.get('card_holder_first_name','')
      card_holder_last_name = alldata.get('card_holder_last_name','')
      card_cvv = alldata.get('card_cvv','')
      card_month = alldata.get('card_month','')
      card_year = alldata.get('card_year','')
      card_type = alldata.get('card_type','')
      card_number = alldata.get('card_number','')
      quantity_val = alldata.get('quantity_val','')
      reservation_total_amt = alldata.get('reservation_total_amt','')
      price=alldata.get('price','')
      reservation_city=alldata.get('reservation_city','')
      one_unit_price=alldata.get('one_unit_price','')
      merchantName=alldata.get('merchant_name','')

      reservation_date=alldata.get('reservation_date','')
      merchant_id=alldata.get('merchant_id','')
      quantity_val=alldata.get('quantity_val','')
      reservation_total_amt=alldata.get('reservation_total_amt','')
      # reservation_total_amt=float(reservation_total_amt)
      reservation_total_amt=0.0
      reservation_total_amt=format(reservation_total_amt, '.2f')
      event_type=alldata.get('special','False')
      reservationDate=alldata.get('reservationDate','')



      my_api = paypalrestsdk.configure({
        # 'mode': config['paypal_mode'],
        # 'client_id': config['paypal_live_client_id'],
        # 'client_secret': config['paypal_live_client_secret']
        'mode': 'sandbox',
        'client_id': 'bnfhgfh',
        'client_secret': 'gbfhdhfgvh'
        
      })


      my_data = {
                  "intent": "sale",
                  "payer": {
                    "payment_method": "credit_card",
                    "funding_instruments": [{
                      "credit_card":{
                        "type": card_type,
                        "number": card_number,
                        "expire_month": card_month,
                        "expire_year": card_year,
                        "cvv2": card_cvv,
                        "first_name": card_holder_first_name,
                        "last_name": card_holder_last_name
                        }
                        }]
                      },
                  "transactions": [{
                    "amount": {
                      "total":reservation_total_amt,
                      "currency": "USD" },
                    "description": "Barlinepass for "+ merchantName+", "+reservation_city }]
                }
    

      payment = paypalrestsdk.Payment(my_data, api=my_api) 
      print payment
      if payment.create():
        state = "Payment is Successful"
        payment_json = str(payment)
        
        # fo = open("payment.txt", "a")
        # fo.write("\n");
        # fo.write("-----------------------------------------------------------------------------");
        # fo.write(payment_json);
        # fo.close()

        return HttpResponseRedirect('/polls/paypal_thanks/?%s' % 'state='+state+'&error='+'none')

      else:
        status = 'Error'
        state = 'Payment Cancelled'

        payment_error = str(payment.error)
        # fo = open("payment.txt", "a")
        # fo.write("\n");
        # fo.write("-----------------------------------------------------------------------------");
        # fo.write(payment_error);
        # fo.close()

        # instance = pmt_summary(text_paypal_payload=payment_error,date=current_date,status=status) 
        # instance.save()

      
  
    return HttpResponseRedirect('/polls/paypal_thanks/?%s' % 'state='+state+'&done='+'none')


def paypal_thanks(request):
    list1 = []
    image_ids = []
  #  mainLayout = MainLayout()
    alldata = request.GET

    url = alldata.get('url')
    state = alldata.get('state')
    state = urllib.unquote(state)
    customer_fname = alldata.get('customer_fname')
    done = alldata.get('done')
    if done!=None:
      return render(request, 'generics/paypal_thanks.html',{'state':state,'customer_fname':customer_fname,'done':done,'url':url})      

    blp_date = alldata.get('blp_date')
    blp_date = urllib.unquote(blp_date)
    img = list(image_ids)
    error = alldata.get('error')
    merchant_name = alldata.get('merchant_name')

    blp_merchant_event_sale_parent_id_thanks = int(alldata.get('blp_merchant_event_sale_parent_id_thanks'))
    try:
      blp_merchant = Merchant_Event_Sale.objects.filter(blp_merchant_event_sale_parent_id=blp_merchant_event_sale_parent_id_thanks)
    except Merchant_Event_Sale.DoesNotExist:
      blp_merchant = None  

    if blp_merchant!=None:
      for val in blp_merchant:
        list1.append(val.blp_merchant_event_sale_scan_hash)
      if list1:
        image_ids = list1  


    return render(request, 'generics/paypal_thanks.html',{'state':state,'image_ids':image_ids,'customer_fname':customer_fname,'merchant_name':merchant_name,'error':error,'url':url,'blp_date':blp_date})
  



def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)  


