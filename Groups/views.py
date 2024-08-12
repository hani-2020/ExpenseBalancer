from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mass_mail
from .models import Group, JoinLink
from Authentications.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

def send_mail_helper(request, recipientlist, group):
    msglist = []
    for reciepent in recipientlist:
        JoinLink.objects.create(group=group, invitee=reciepent)
        subject = f"Invitation to join expense group: {group.group_name}"
        message = f"""
        {request.user.username} has invited you to join their expense group.
        To join click this link:{settings.SITE_URL}/groups/join_group/{group.id}/{reciepent.id}
        """
        reciever = [reciepent.email]
        msg = (subject, message, "admin@expensemanager.com", reciever)
        msglist.append(msg)
    send_mass_mail(tuple(msglist), fail_silently=False)

@login_required
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
        if friendslist:
            recipientlist = [User.objects.get(id=id) for id in friendslist]
            send_mail_helper(request, recipientlist, group)
        group.save()
    return render(request, 'create_groups.html', context)

@login_required
def view_groups(request):
    context = {}
    groups = request.user.group_members.all()
    context['groups'] = groups
    return render(request, 'view_groups.html', {'groups':groups})

@login_required
def edit_group(request, id):
    context = {}
    group = Group.objects.get(id=id)
    context['group'] = group
    members = group.members.all()
    friends = request.user.friends.exclude(id__in=members)
    context['friends'] = friends
    if request.method=='POST' and request.user==group.created_by:
        group_name = request.POST.get('group_name').strip()
        if group_name=="":
            context['error'] = 'Group must have a name'
            return render(request, 'create_groups.html', context)
        friends = request.POST.getlist('friends')
        group.group_name = group_name
        if friends:
            recipientlist = [User.objects.get(id=id) for id in friends]
            send_mail_helper(request, recipientlist, group)
        group.save()
        return redirect('view_groups')
    return render(request, 'create_groups.html', context)

@login_required
def delete_group(request, id):
    group = Group.objects.get(id=id)
    if request.user == group.created_by:
        group.delete()
    return redirect('view_groups')

@login_required
def leave_group(request, id):
    group = Group.objects.get(id=id)
    if request.user != group.created_by:
        group.members.remove(request.user)
    return redirect('view_groups')

@login_required
def join_group(request, group_id, user_id):
    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    joinlink = JoinLink.objects.filter(group=group, invitee=user)
    if request.user==user and joinlink.exists():
        group.members.add(request.user)
        group.save()
        joinlink.delete()
    elif request.user!=user:
        return HttpResponse("Not your invite")
    return redirect('homepage')