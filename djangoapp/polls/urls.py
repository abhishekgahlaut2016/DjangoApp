from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_user/$', views.register_user, name='register_user'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^image_detail/$', views.image_detail, name='image_detail'),
    url(r'^add_to_cart/$', views.add_to_cart, name='add_to_cart'),
    url(r'^cart_items/$', views.cart_items, name='cart_items'),
    url(r'^products/$', views.products, name='products'),
    url(r'^buy_product/$', views.buy_product, name='buy_product'),
    url(r'^payment/$', views.make_payment, name='make_payment'),
    url(r'^paypal_process/$', views.paypal_process, name='paypal_process'),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),    
]