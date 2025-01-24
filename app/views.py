from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login

from .models import *
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

def send_otp(email):
    otp=random.randint(100000,999999)
    send_mail(
        'Your OTP Code',''
        f'Your OTP code is: {otp}',
        'avanthikaanilkumar18@gmail.com',
        [email],
        fail_silently=False,
    )
    return otp

def password_reset_request(request):
    if request.method =='POST':
        email=request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp=send_otp(email)

            context={
                "email":email,
                "otp": otp,
            }
            return render(request,'forgot_password2.html',context)
        
        except User.DoesNotExist:
            messages.error(request,'Email address not found.')
    else:
        return render(request,'forgot_password1.html')
    return render(request,'forgot_password1.html')

def verify_otp(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        otpold=request.POST.get('otp1')
        otp=request.POST.get('otp2')

        if otpold==otp:
            context={
                'otp' : otp,
                'email' : email
            }
            return render(request,'forgot_password3.html',context)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,'forgot_password2.html')

def set_new_password(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        new_password=request.POST.get('password1')
        confirm_password=request.POST.get('password2')
        if new_password==confirm_password:
            try:
                user=User.objects.get(email=email)
                
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password has been reset successfully')
                return redirect(user_login)
            except User.DoesNotExist:
                messages.error(request,'Password does not match')
        return render(request,'forgot_password3.html',{'email':email})
    return render(request,'forgot_password3.html',{'email':email})



def index(request):
    return render(request,'index.html')

def user_registration(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        
        email=request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return render(request,'registration.html',{'error':'Email already exisits'})
        phone_no=request.POST.get('no')
        if User_details.objects.filter(phone_number=phone_no).exists():
            return render(request,'registration.html',{'error':'Phone number already exists'})

        gender=request.POST.get('gender')
        address=request.POST.get('address')
        uname=request.POST.get('uname')
        if User.objects.filter(username=uname).exists():
            return render(request,'registration.html',{'error':'Username already exists'})
        password=request.POST.get('password')
        cpass=request.POST.get('cpass')
        if password!=cpass:
            return render(request,'registration.html',{'error':'password already exists'})
        data=User.objects.create_user(first_name=name,username=uname,password=password,email=email)
        data.save()
        data1=User_details.objects.create(user_id=data,phone_number=phone_no,gender=gender,address=address)
        data1.save()
        return redirect('log')
    else:
        return render(request,'registration.html')




def user_login(request):
    if request.method == 'POST':
        username=request.POST.get('uname')
        password=request.POST.get('password')
        data=authenticate(username=username,password=password)
        admin_user=authenticate(request,username=username,password=password)
        if admin_user is not None and admin_user.is_staff:
            login(request,admin_user)
            return redirect('adminhome')
        
        elif data is not None:
            login(request,data)
            return redirect('userhome')
        else:
            return HttpResponse('invalid username or paasword')
    else:
        return render(request,'Login.html')
def user_home(request):
    return render(request,'userhome.html')


def view_user(request):
    user=User.objects.get(id=request.user.id)
    val=User_details.objects.get(user_id=user.id)
    return render(request,'viewuser.html',{'data':val})
   



# admin.......................

def admin_home(request):
    return render(request,'adminhome.html')

def user_details(request):
    data=User_details.objects.all()
    return render(request,'user_details.html',{'data':data})

def view_hall(request):
    data=Halls.objects.all()
    return render(request,'view_hall.html',{'data':data})

def add_hall(request):
    if request.method == 'POST':
        hall_name=request.POST.get('name')
        location=request.POST.get('location')
        print("location = ",location)
        capacity=request.POST.get('capacity')
        price_per_day=request.POST.get('price_per_day')
        photo_url=request.FILES['photo_url']
        hall_description=request.POST.get('hall_description')
        data=Halls.objects.create(hall_name=hall_name,location=location,capacity=capacity,price_per_day=price_per_day,photo_url=photo_url,hall_description=hall_description)
        data.save()
        return redirect('hall')
    else:
        return render(request,'add_hall.html')
    
def food(request):
    data=Food.objects.all()
    return render(request,'food.html',{'data':data})

def add_food(request):
    if request.method=='POST':
        name=request.POST['name']
        image=request.FILES['image']
        price=request.POST['price']
        val=Food.objects.create(food_name=name,food_image=image,food_price=price)
        val.save()
        return redirect('food')
    else:
        return render(request,'add_food.html')
def decoration_details(request):
    data=Decoration.objects.all()
    return render(request,'decoration_details.html',{'data':data})
def add_decoration(request):
    if request.method == 'POST':
        name=request.POST['name']
        price=request.POST['price']
        image=request.FILES['image']
        obj=Decoration.objects.create(decoration_name=name,decoration_price=price,decoration_image=image)
        obj.save()
        return redirect(decoration_details)
    return render(request,'add_decoration.html')







