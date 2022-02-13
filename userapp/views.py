from django.shortcuts import redirect, render
from .forms import User,UpdateUser,FileUploadForm
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .backends import UserAuthenticate
from .task import *
from django.contrib.auth.decorators import login_required


# Create your views here.

def my_login(request):
    form=User()
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        check_user=UserAuthenticate()
        myuser=check_user.authenticate(email,password)
        print(myuser)
        if myuser is not None and myuser.is_superuser or request.method=='GET':
            login(request,myuser)
            return redirect('adminpage')
        elif myuser is not None and myuser.is_active:
            login(request,myuser)
            return redirect('userpage')
        elif myuser is not None and not myuser.is_active:
            messages.warning(request,'you are not allowed by admin')
            return render(request,'login.html',{'form':form})
        elif myuser is None:
            messages.warning(request,'email/password is invalid')
            return render(request,'login.html',{'form':form})
    return render(request,'login.html',{'form':form})


@login_required(login_url='login')
def updateuser(request,id):
    user=CustomUser.objects.get(id=id)
    form=UpdateUser(instance=user)
    if request.method=='POST':
        data=UpdateUser(request.POST,instance=user)
        if data.is_valid():
            data.save()
            user=data.cleaned_data.get('email')
            is_active=data.cleaned_data.get('is_active')
            if is_active:
               mail.delay(user)
            else:
                login_not_allowed_mail.delay(user)
            return redirect('adminpage')
    return render(request,'userupdate.html',{'user':form})



@login_required(login_url='login')
def user_logout(request):
       logout(request)
       return redirect('/')


@login_required(login_url='login')
def userpage(request):
    form=FileUploadForm()
    if request.method=='POST':
        data=request.FILES['file_upload']
        form=FileUploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            filepath=f'{settings.MEDIA_ROOT}/documents/{data}'
            savedata.delay(filepath)
            print('upload file1')
            return render(request,'userpage.html',{'form':form})
    return render(request,'userpage.html',{'form':form})
    

@login_required(login_url='login')
def adminpage(request):
    user=CustomUser.objects.filter(is_superuser=False)
    return render(request,'adminpage.html',{'user':user})




