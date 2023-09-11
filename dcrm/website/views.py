from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import SignUpForm, AddRecordForm
from . models import Records


# Create your views here.
def home(request):
    records = Records.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"Logged in Successful")
            return redirect('home')
        else:
            messages.success(request, 'error credential')
            return redirect('home')
        
    else:
        return render(request, 'home.html', {'records':records})
  


def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged out!...')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #automate login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have signed in!')
            return redirect('home')
    else:
        form = SignUpForm()
        
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Records.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, 'You must log in...')
        return redirect('home')
    
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Records.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('home')
    else:
        messages.success(request, 'You must log in...')
        return redirect('home')
    

def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm()
        if request.method == 'POST':
            form = AddRecordForm(request.POST)
            if form.is_valid:
                form.save()
                messages.success(request, 'Record Added')
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, 'You must login to add record...')
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        record = get_object_or_404(Records, id=pk)
        if request.method == 'POST':
            form = AddRecordForm(request.POST, instance=record)
            if form.is_valid:
                form.save()
                messages.success(request, 'Updated Successfully..!')
                return redirect('home')
            
        else:
            form = AddRecordForm(instance=record)
        return render(request, 'update_record.html', {'form': form, 'record': record})
    else:
        messages.success('You must logged in..!')
        return redirect('home')
        
    
    
    
    