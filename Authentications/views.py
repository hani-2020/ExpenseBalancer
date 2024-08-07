from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from Expenses.models import Split, Expenses
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if not request.user.is_authenticated:
        return HttpResponse("Not authorized")
    incoming_payments = []
    outgoing_payments = []
    outgoing_splits = Split.objects.filter(payer=request.user)
    for outgoing_split in outgoing_splits:
        if outgoing_split.expense.paid_by != request.user:
            outgoing_payments.append(outgoing_split)
    incoming_expenses = Expenses.objects.filter(paid_by=request.user)
    for incoming_expense in incoming_expenses:
        incoming_splits = Split.objects.filter(expense=incoming_expense)
        for incoming_split in incoming_splits:
            if incoming_split.payer != incoming_expense.paid_by:
                incoming_payments.append(incoming_split)
    context = {
        "incoming_payments":incoming_payments[:5],
        "outgoing_payments":outgoing_payments[:5]
    }
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
