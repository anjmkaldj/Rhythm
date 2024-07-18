from django.urls import path
from .views import *
from .import views

urlpatterns=[
    path('index/',index),
    path('reg/',reg),
    path('userlogin/',userlogin),
    path('profile/',profile),
    path('profileview/',profileview),
    path('updatedetails/',updatedetails),
    path('songs/',songs),
    path('itemdisplay/',itemdisplay),

    path('edit/<int:id>',edit),


    path('addtowishlist/<int:itemid>',addtowishlist),
    path('wishlist/',wishlist),
    path('removewishlist/<int:itemid>',removewishlist),
    path('wishtoaddtocart/',wishtoaddtocart),

    path('order_view/',order_view),
    path('create_order/',create_order),
    path('record_and_combine/<int:karaoke_id>/', views.record_and_combine_audio, name='record_and_combine'),
    path('recordings_list/', views.recordings_list, name='recordings_list'),



    path('logout/',logout)





]