from django.shortcuts import render, redirect
from Groups.models import Group
from .models import Expenses, Split
from Authentications.models import User

def save_split_helper(request, key, percents_or_amounts, expense, splits):
    if key != 'csrfmiddlewaretoken':
        rate_or_amount = request.POST.get(key)
        if rate_or_amount:
            rate_or_amount = float(rate_or_amount)
            percents_or_amounts.append(rate_or_amount)
            member = User.objects.get(id=key)
            if expense.split_method==2:
                amount = float(expense.amount) * rate_or_amount/100
            if expense.split_method==3:
                amount = rate_or_amount
            split = Split(payer=member, expense=expense, amount=amount)
            splits.append(split)

def create_expense(request, id):
    group = Group.objects.get(id=id)
    members = group.members.all()
    context = {
    'group': group,
    'members': members,
    }
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        paid_by = request.POST.get('paidby')
        paid_by = User.objects.get(id=paid_by)
        split_method = int(request.POST.get('splitmethod'))
        if not amount:
            context['error'] = "Amount field must not be empty"
            return render(request, 'create_expense.html', context)
        expense = Expenses.objects.create(amount=amount,
                                          description=description,
                                          paid_by=paid_by, group=group,
                                          split_method=split_method)
        if date:
            expense.date = date
        expense.save()
        context['expense'] = expense
        if split_method == 1:
            amount = int(amount)/len(members)
            context['amount'] = amount
        return render(request, 'split_details.html', context)
    return render(request, 'create_expense.html', context)

def save_split(request, expense_id):
    expense = Expenses.objects.get(id=expense_id)
    members = expense.group.members.all()
    context = {
        'expense':expense,
        'members':members
    }
    if request.method=='POST':
        if expense.split_method == 1:
            amount = expense.amount/len(members)
            for member in members:
                Split.objects.create(payer=member, expense=expense, amount=amount)
        elif expense.split_method == 2:
            percents = []
            splits = []
            for key in request.POST:
                save_split_helper(request, key, percents, expense, splits)
            if sum(percents) != 100:
                context['error'] = 'Divison does not reach 100%'
                return render(request, 'split_details.html', context)
            for split in splits:
                split.save()
        elif expense.split_method == 3:
            amounts  = []
            splits = []
            for key in request.POST:
                save_split_helper(request, key, amounts, expense, splits)
            if sum(amounts) != expense.amount:
                context['error'] = 'Divison does not reach full amount'
                return render(request, 'split_details.html', context)
            for split in splits:
                split.save()
    return redirect('view_groups')

def view_expenses(request):
    splits =  Split.objects.filter(payer=request.user)
    expenses = []
    for split in splits:
        expenses.append(split.expense)
    context = {'splits':splits}
    return render(request, 'view_expenses.html', context)

def view_group_expenses(request, group_id):
    expenses = Expenses.objects.filter(group=group_id)
    expense_list = []
    for expense in expenses:
        object = {
            'expense':expense,
            'split':expense.expenses_split.filter(payer=request.user).first(),
        }
        expense_list.append(object)
    context = {'expense_list':expense_list}
    return render(request, 'view_group_expenses.html', context)

#to do
#join group emails (like my blackjack app)
#paid_by user should not be billed instead it should show how much he should be payed (he can be given neagtive balnce equal to the 
# total amount remove him from the split pages, if conditions will check if member is paidby user and do what is required)
#only paid_by user can edit and delete expense (have not implemented edit or delete functionality)
#display amount of money to give, recieve and the people associated with it (doing no.2 will do alot of this)
#dashboard (doing no.2 will do alot of this)
#unit testing (must learn, will probably have to add alot of validations, change login page to forms)
#remove unwanted fields from models
#ui (make this look cleaner. bootstrap???)