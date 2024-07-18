from django.urls import path
from .views import *


urlpatterns=[
    path('registercreator/',register_creator),
    path('loginview/',login_view),
    path('creatorindex/',creatorindex),
    path('creatorprofile/',creatorprofile),
    path('itemdelete/<int:itemid>',removeitem),
    path('itemedit/<int:id>',edit),
    path('songs/',songs)

]