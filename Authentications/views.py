from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from Expenses.models import Split
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    context = {}
    if request.user.is_authenticated:
        splits = Split.objects.filter(payer=request.user)[:5]
        context["splits"] = splits
    return render(request, 'home.html', context)

def signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'signup.html', {'form':form})

def userlogin(request):
    messages = {}
    if '/groups/join_group/' in request.get_full_path():
        path = request.get_full_path()[32:]
        end = path.find('/')
        messages['joingroup'] = path[:end]
        messages['joingroupuser'] = path[end+1:]
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            group_id = request.POST.get('group_id')
            user_id = request.POST.get('user_id')
            if group_id:
                return redirect(f'/groups/join_group/{group_id}/{user_id}')
            return redirect('homepage')
        messages['error'] =' invalid credentials'
    return render(request, 'login.html', messages)
