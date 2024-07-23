from django.shortcuts import render
from Authentications.models import User
from django.db.models import Q

def friends_page(request):
    results = None
    if request.method == 'POST':
        results = User.objects.filter(Q(username__icontains=request.POST['search']) | Q(email__icontains=request.POST['search']))
    return render(request, 'friends.html', {'results':results})
