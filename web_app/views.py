from django.shortcuts import render,redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Records
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def home(request):
    return render(request, 'web_app/index.html')

#Register a user
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Created Successfully!")
            return redirect('my_login')
    context = {'form':form}
    return render(request,'web_app/register.html',context=context)

# login User
def my_login(request):
    form = LoginForm()
    if request.method == "POST":
        form= LoginForm(request, data=request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request,"You have loged in")
                return redirect('dashboard')
    context={'form':form}
    return render(request,'web_app/my-login.html',context=context)


# Dashboard
@login_required(login_url='my_login')
def dashboard(request):
    records_per_page = 5
    all_records= Records.objects.all()
    search_query = request.GET.get('q')
    if search_query:
     all_records = all_records.filter(Q(first_name__icontains=search_query))
    paginator = Paginator(all_records, records_per_page)
    page = request.GET.get('page')
    try:
        my_records=paginator.page(page)
    except PageNotAnInteger:
        my_records=paginator.page(1)
    except EmptyPage:
        my_records=paginator.page(paginator.num_pages)
    context={'records':my_records, 'search_query': search_query}
    return render(request, 'web_app/dashboard.html',context=context)

# Logout
def user_logout(request):
    auth.logout(request)
    messages.success(request,"Logout success!")
    return redirect('my_login')

# Create a record
@login_required(login_url='my_login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your record created!")
            return redirect("dashboard")
        
    context= {'form':form}
    return render(request, 'web_app/create-record.html', context=context)

# Update record
@login_required(login_url='my_login')
def update_record(request, pk):
    record = Records.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method =='POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request,"Your record was updated sucessfully!")
            return redirect("dashboard")
    context={'form':form}
    return render(request, 'web_app/update-record.html', context=context)

# View Record
@login_required(login_url='my_login')
def singular_record(request, pk):
    all_records=Records.objects.get(id=pk)
    context={'record':all_records}
    return render(request,'web_app/view-record.html',context=context)

# Delete Record
@login_required(login_url='my_login')
def delete_record(request, pk):
    record=Records.objects.get(id=pk)
    record.delete()
    messages.success(request,"Your record was deleted!")
    return redirect("dashboard")