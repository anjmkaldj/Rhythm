from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm
from musicapp.models import *
from django.http import HttpResponse

# Create your views here.
# def register_sellers(request):
#     return render(request,'seller_register.html',{'form':CreatorRegistrationForm()})


def register_creator(request):
    if request.method=='POST':
        form =CreatorRegistrationForm(request.POST)
        if form.is_valid():
            #in django is_valid is a method used with forms to check if the data provided meets the validation criteria.
            password=form.cleaned_data.get('password')
            cpassword=form.cleaned_data.get('cpassword')
            if password!=cpassword:
                messages.error(request,"password don't match")

                  #cleaned datas refers to the validated datas that has been submitted through form.The forms cleaned data attribute is populated when the datas are passes the isvalid method.
            else:
                user=form.save(commit=False)
                user.set_password(password)
                user.save()

                messages.success(request,"Registration successful.You can now log in")
                return HttpResponse("registration success")
    else:

        form=CreatorRegistrationForm()  #storing our form
    return render(request,'register.html',{'form':form})
#if the method is not post
#if the form is not valid
#if password is incorrect
#success



def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)


            if user is not None:
                login(request,user)
                #login(): function used to login authenticated system
                request.session['creatorid']=user.id

                messages.success(request,f'you are now logged in as {username}.')
                return redirect(creatorprofile)
            else:
                messages.error(request,'Invalid username or password')
        else:
            messages.error(request,'form is not valid')
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})

def creatorindex(request):
    return render(request,'creatorindex.html')

def creatorprofile(request):
    id=request.session['creatorid']
    data = User.objects.get(id=id)
    category = request.GET.get('category', 'all')
    if category == 'all':
        db = karoakedetails.objects.all()
    else:
        db = karoakedetails.objects.filter(category=category)


    for item in db:
        item.avail_sizes = item.avail_sizes.split(',')

    return render(request,'creatorprofile.html',{'data':data,'db':db})


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
        return render(request,'creatoritemadd.html')


def removeitem(request,itemid):
    db=karoakedetails.objects.get(id=itemid)
    db.delete()
    return redirect(creatorprofile)

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

        return redirect(creatorprofile)
    return render(request,'updateitem.html',{'data':db})
