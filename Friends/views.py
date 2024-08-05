from django.shortcuts import render, redirect
from Authentications.models import User
from django.db.models import Q
from .models import FriendRequests
from django.contrib.auth.decorators import login_required

@login_required
def friends_page(request):
    context = {}
    if request.method == 'POST':
        search_query = request.POST.get('search').strip()
        if search_query:
            results = User.objects.filter(Q(username__icontains=search_query) | Q(email__icontains=search_query))
            friend_ids = request.user.friends.values_list('id', flat=True)
            results = results.exclude(Q(id=request.user.id) | Q(id__in=friend_ids))
            context['results'] = results
        else:
            context['error'] = 'No such user'
    return render(request, 'friends.html', context)

@login_required
def send_request(request, id):
    to_user = User.objects.get(id=id)
    if not FriendRequests.objects.filter(from_user=request.user, to_user=to_user).exists():
        FriendRequests.objects.create(from_user=request.user, to_user=to_user)
    return redirect(friends_page)

@login_required
def pending_requests(request):
    pending_requests = FriendRequests.objects.filter(to_user=request.user)
    return render(request, 'pending_requests.html', {'pending_requests':pending_requests})

@login_required
def accept_request(request, id):
    friend = FriendRequests.objects.get(id=id)
    if request.user == friend.to_user:
        friend.from_user.friends.add(friend.to_user)
        friend.save()
        friend.delete()
    return redirect(pending_requests)

@login_required
def reject_request(request, id):
    friend = FriendRequests.objects.get(id=id)
    if request.user == friend.to_user:
        friend.delete()
    return redirect(pending_requests)

@login_required
def see_friends(request):
    friends = request.user.friends.all()
    return render(request, 'see_friends.html', {'friends':friends})