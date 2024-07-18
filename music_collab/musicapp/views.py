from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import UserReg

from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# import stripe

import pyaudio
import wave

# Create your views here.
def index(request):
    return render(request,'index.html')




def reg(request):
    if(request.method=='POST'):
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        propic=request.FILES.get('propic')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if(password==cpassword):
            data=UserReg(fn=fullname,em=email,ph=phone,pro_pic=propic,password=password)
            data.save()
            return redirect(userlogin)
        else:
            return HttpResponse("registration failed")
    return render(request,'registration.html')


def userlogin(request):
    if(request.method=="POST"):
        email=request.POST.get('email')
        password=request.POST.get('password')
        data=UserReg.objects.all()
        for i in data:
            if(i.em==email and i.password==password):
                request.session['userid']=i.id
                return redirect(itemdisplay)
        else:
            return HttpResponse('login failed')

    return render(request,'userlogin.html')


def profile(request):
    category = request.GET.get('category', 'all')
    if category == 'all':
        db = karoakedetails.objects.all()
    else:
        db = karoakedetails.objects.filter(category=category)
    songs = [
        {'title': 'Song 1', 'artist': 'Artist 1', 'cover_image': 'images/music-cover.jpg', 'play_url': '#'},
        {'title': 'Song 2', 'artist': 'Artist 2', 'cover_image': 'images/music-cover.jpg', 'play_url': '#'},
        # Add more songs as needed
    ]
    return render(request, 'profile.html', {'songs': songs})






def profileview(request):
    id1=request.session['userid']
    db=UserReg.objects.get(id=id1)
    return render(request,'profileview.html',{'data':db})


def updatedetails(request):
    id1=request.session['userid']
    db=UserReg.objects.get(id=id1)
    if(request.method=='POST'):

        if(request.FILES.get('propic')==None):

            db.save()
        else:
            db.pro_pic = request.FILES.get('propic')

        db.fn = request.POST.get('fullname')
        db.em = request.POST.get('email')
        db.ph = request.POST.get('phone')
        db.save()
        return redirect(profileview)
    return render(request,'updateuserprofile.html',{'data':db})

def songs(request):
    if(request.method=="POST"):
        song_name=request.POST.get('songname')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        des= request.POST.get('des')
        category = request.POST.get('category')
        mp3_file = request.FILES.get('mp3_file')
        db=karoakedetails(song_name=song_name,price=price,image=image,des=des,category=category,mp3_file=mp3_file)
        db.save()
        return HttpResponse('song added')
    else:
        return render(request,'itemadd.html')

def itemdisplay(request):
    id1 = request.session['userid']
    d = UserReg.objects.get(id=id1)

    category = request.GET.get('category', 'all')
    if category == 'all':
        db = karoakedetails.objects.all()
    else:
        db = karoakedetails.objects.filter(category=category)
    return render(request,'itemdisplay.html',{'db':db,'d':d,'data':db})


def edit(request,id):

    db=karoakedetails.objects.get(id=id)
    if(request.method=='POST'):

        if(request.FILES.get('image')==None):

            db.save()
        else:
            db.image = request.FILES.get('image')

        db.prod_name = request.POST.get('songname')
        db.price = request.POST.get('price')
        db.des = request.POST.get('des')
        db.category = request.POST.get('category')

        db.save()

        return redirect(itemdisplay)
    return render(request,'updateitem.html',{'data':db})




def addtowishlist(request,itemid):
    item=karoakedetails.objects.get(id=itemid)

    list=Wishlist.objects.all()
    for i in list:
        if i.item.id==itemid and i.userid==request.session['userid']:
           return redirect(wishlist)
    else:
        db=Wishlist(userid=request.session['userid'],item=item)#avail_sizes=sizes
        db.save()
        return redirect(itemdisplay)



def wishlist(request):
    list=Wishlist.objects.all()
    return render(request,'wishlistdisplay.html',{'db':list})

def removewishlist(request,itemid):
    db=Wishlist.objects.get(id=itemid)
    db.delete()
    return redirect(wishlist)

def wishtoaddtocart(request):
    return redirect(wishlist)

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_order(request):
    if request.method == 'POST':
        userid = request.session['userid']  # Assuming userid is stored in session
        user = UserReg.objects.get(id=userid)


        # Create the order object
        order = OrderItem.objects.create(userdetails=user)

        # Calculate total price or use a fixed amount
        total_price = 100 # Replace with your dynamic calculation or fixed amount

        # Calculate expected delivery date
        expected_delivery_date = datetime.now() + timedelta(days=7)

        # Construct email content
        subject = 'Order Confirmation'
        context = {
            'total_price': total_price
        }
        html_message = render_to_string('order_confirmation_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'your-email@example.com'
        to_email = [user.email]

        # Send email
        send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

        # Create a Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Order Payment',  # Replace with your product name
                        },
                        'unit_amount': int(total_price * 100),  # Convert to cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/payment/success/'),  # Redirect URL after successful payment
            cancel_url=request.build_absolute_uri('/payment/cancel/'),  # Redirect URL if payment is canceled
        )

        # Redirect to Stripe checkout session
        return redirect(checkout_session.url)

    # Handle GET request if needed
    return JsonResponse({'error': 'Invalid Request'}, status=400)


def order_view(request):
    userid=request.session['userid']
    order=OrderItem.objects.filter(order__userdetails__id=userid).order_by('-order__ordered_date')
    return render(request,'order.html',{'order':order})

# views.py

import os


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import UserReg, karoakedetails, AudioRecording
from .forms import AudioRecordingForm
from pydub import AudioSegment

from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from pydub import AudioSegment
from .forms import AudioRecordingForm
from .models import karoakedetails, AudioRecording
import os

def record_and_combine_audio(request, karaoke_id):
    karaoke = get_object_or_404(karoakedetails, id=karaoke_id)
    if request.method == 'POST':
        form = AudioRecordingForm(request.POST, request.FILES)
        if form.is_valid():
            recording = form.save(commit=False)
            recording.background_file = karaoke.mp3_file
            recording.save()

            try:
                # Combine the audio files
                background = AudioSegment.from_file(recording.background_file.path)
                voice = AudioSegment.from_file(recording.voice_recording.path)

                # Ensure both files are in the same format
                if background.frame_rate != voice.frame_rate:
                    voice = voice.set_frame_rate(background.frame_rate)

                # Combine the audio files
                combined = background.overlay(voice)

                # Save the combined audio file
                combined_file_path = f'combined/{recording.id}_combined.mp3'
                combined_audio = combined.export(format='mp3')
                combined_audio_content = ContentFile(combined_audio.read())

                # Ensure the 'combined' directory exists
                os.makedirs(os.path.dirname(combined_file_path), exist_ok=True)

                recording.combined_file.save(combined_file_path, combined_audio_content)
                recording.save()

                return redirect('recordings_list')
            except FileNotFoundError as e:
                return render(request, 'record_and_combine.html', {'form': form, 'karaoke': karaoke, 'error': "Audio file not found."})

    else:
        form = AudioRecordingForm()

    return render(request, 'record_and_combine.html', {'form': form, 'karaoke': karaoke})

from django.shortcuts import render
from .models import AudioRecording

def recordings_list(request):
    recordings = AudioRecording.objects.all()
    return render(request, 'recordings_list.html', {'recordings': recordings})



def logout(request):
    request.session.flush()
    return redirect(index)



