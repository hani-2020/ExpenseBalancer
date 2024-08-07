from django.shortcuts import render, redirect
from Groups.models import Group
from .models import Expenses, Split
from Authentications.models import User
from django.contrib.auth.decorators import login_required

def save_split_helper(request, key, percents_or_amounts, expense, splits):
    if key != 'csrfmiddlewaretoken':
        rate_or_amount = request.POST.get(key)
        if rate_or_amount:
            rate_or_amount = float(rate_or_amount)
            percents_or_amounts.append(rate_or_amount)
            member = User.objects.get(id=key)
            if expense.split_method==2:
                amount = float(expense.amount) * rate_or_amount/100
            elif expense.split_method==3:
                amount = rate_or_amount
            split = Split(payer=member, expense=expense, amount=amount)
            splits.append(split)

@login_required
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

@login_required
def save_split(request, expense_id):
    expense = Expenses.objects.get(id=expense_id)
    Split.objects.filter(expense=expense).delete()
    members = expense.group.members.all()
    context = {
        'expense':expense,
        'members':members
    }
    if request.method=='POST' and request.user == expense.paid_by:
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
    return render(request, 'split_details.html', context)

@login_required
def view_expenses(request):
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
        "incoming_payments":incoming_payments,
        "outgoing_payments":outgoing_payments
    }
    return render(request, 'view_expenses.html', context)

@login_required
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

@login_required
def view_expense_breakup(request, expense_id):
    expense = Expenses.objects.get(id=expense_id)
    splits = Split.objects.filter(expense=expense)
    for split in splits:
        split.amount = abs(split.amount)
    context = {'expense':expense,
               'splits':splits}
    return render(request, 'view_expense_breakup.html', context)

@login_required
def edit_expense(request, expense_id):
    expense = Expenses.objects.get(id=expense_id)
    group = Group.objects.get(id=expense.group.id)
    members = group.members.all()
    context = {'expense':expense, 'group':group, 'members':members}
    if request.method == 'POST' and request.user == expense.paid_by:
        expense.amount = float(request.POST.get('amount'))
        expense.description = request.POST.get('description')
        date = request.POST.get('date')
        if date:
            expense.date = date
        paid_by = request.POST.get('paidby')
        expense.paid_by = User.objects.get(id=paid_by)
        expense.split_method = int(request.POST.get('splitmethod'))
        expense.save()
        if expense.split_method == 1:
            amount = int(expense.amount)/len(members)
            context['amount'] = amount
        return render(request, 'split_details.html', context)
    return render(request, 'create_expense.html', context)

@login_required
def delete_expense(request, expense_id):
    expense = Expenses.objects.get(id=expense_id)
    if request.user == expense.paid_by:
        expense.delete()
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)

@login_required
def pay_expense(request, split_id):
    split = Split.objects.get(id=split_id)
    context={}
    if split.payer != request.user:
        context['error'] = "You can't pay that split"
        return render(request, 'view_expense_breakup.html', context)
    split.delete()
    return redirect('homepage')

@login_required
def debtors_creditors(request):
    # splits = Split.objects.filter(payer=request.user)
    # expenses = []
    # for split in splits:
    #     expenses.append(split.expense)
    # friends = []
    # for expense in expenses:
    #     splits = Split.objects.filter(expense=expense)
    #     for split in splits:
    #         if split.payer != request.user and split.payer not in friends:
    #             friends.append(split.payer)
    friends = []
    expenses = Expenses.objects.filter(paid_by=request.user)
    for expense in expenses:
        splits = Split.objects.filter(expense=expense)
        for split in splits:
            if split.payer != request.user and split.payer not in friends:
                friends.append(split.payer)
    splits = Split.objects.filter(payer=request.user)
    expenses = []
    for split in splits:
        expenses.append(split.expense)
    for expense in expenses:
        splits = Split.objects.filter(expense=expense)
        for split in splits:
            if split.payer != request.user and split.payer not in friends:
                friends.append(split.payer)
            if expense.paid_by != request.user and expense.paid_by not in friends:
                friends.append(expense.paid_by)
    return render(request, 'see_friends.html', {'friends':friends})