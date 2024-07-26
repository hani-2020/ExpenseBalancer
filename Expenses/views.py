from django.shortcuts import render, redirect
from Groups.models import Group
from .models import Expenses, Split
from Authentications.models import User

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
        split_method = request.POST.get('splitmethod')
        if not amount:
            context['error'] = "Amount field must not be empty"
            return render(request, 'create_expense.html', context)
        expense = Expenses.objects.create(amount=amount, description=description, date=date, paid_by=paid_by, group=group, split_method=split_method)
        expense.save()
        context['expense'] = expense
        if split_method=='1':
            amount = int(amount)/len(members)
            context['amount'] = amount
        return render(request, 'split_details.html', context)
    return render(request, 'create_expense.html', context)

def save_split(request, expense_id):
    if request.method=='POST':
        expense = Expenses.objects.get(id=expense_id)
        if expense.split_method == 1:
            members = expense.group.members.all()
            amount = expense.amount/len(members)
            for member in members:
                Split.objects.create(payer=member, expense=expense, amount=amount)
            return redirect('view_groups')