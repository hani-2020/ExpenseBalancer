from django.shortcuts import render

def create_expense(request):
    return render(request, 'create_expense.html')
