from django.shortcuts import render
from .models import Group

def create_groups(request):
    context = {}
    friends = request.user.friends.all()
    context['friends'] = friends
    if request.method=='POST':
        group_name = request.POST.get('group_name').strip()
        if group_name=="":
            context['error'] = 'Group must have a name'
            return render(request, 'create_groups.html', context)
        friendslist = request.POST.getlist('friends')
        group = Group.objects.create(group_name=group_name)
        group.members.add(request.user)
        group.members.add(*friendslist)
    return render(request, 'create_groups.html', context)
