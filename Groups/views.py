from django.shortcuts import render, redirect
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
        group = Group.objects.create(group_name=group_name, created_by=request.user)
        group.members.add(request.user)
        group.members.add(*friendslist)
        group.save()
    return render(request, 'create_groups.html', context)

def view_groups(request):
    context = {}
    groups = request.user.group_members.all()
    context['groups'] = groups
    return render(request, 'view_groups.html', {'groups':groups})

def edit_group(request, id):
    context = {}
    group = Group.objects.get(id=id)
    context['group'] = group
    members = group.members.all()
    friends = request.user.friends.exclude(id__in=members)
    context['friends'] = friends
    if request.method=='POST':
        group_name = request.POST.get('group_name').strip()
        if group_name=="":
            context['error'] = 'Group must have a name'
            return render(request, 'create_groups.html', context)
        friends = request.POST.getlist('friends')
        group.group_name = group_name
        if friends:
            group.members.add(*friends)
        group.save()
        return redirect('view_groups')
    return render(request, 'create_groups.html', context)

def delete_group(request, id):
    group = Group.objects.get(id=id)
    if request.user == group.created_by:
        group.delete()
    return redirect('view_groups')

def leave_group(request, id):
    group = Group.objects.get(id=id)
    if request.user != group.created_by:
        group.members.remove(request.user)
    return redirect('view_groups')
