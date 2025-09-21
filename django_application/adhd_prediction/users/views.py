from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username} now you can login')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

def custom_logout(request): 
    logout(request) 
    return render(request,'users/logout.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)#the user update form that will update the username and the email
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        #updating the profile picture
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'your account has been updated')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)#the user update form that will update the username and the email
        p_form=ProfileUpdateForm(instance=request.user.profile)#updating the profile picture
    

    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'users/profile.html',context)

# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error
