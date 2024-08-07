from django.shortcuts import render, redirect
from Authentications.models import User
from django.db.models import Q
from .models import FriendRequests
from Expenses.models import Split
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
            if results:
                context['results'] = results
            else:
                context['error'] = 'No such user available'
        else:
            context['error'] = 'Enter a username or email'
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

@login_required
def see_friend_transanctions(request, user_id):
    user = User.objects.get(id=user_id)
    splits = user.expenses_payer.all()
    context = {'friend':user}
    incoming_payments = []
    for split in splits:
        if split.expense.paid_by == request.user:
            incoming_payments.append(split)
    context['incoming_payments'] = incoming_payments
    splits = request.user.expenses_payer.all()
    outgoing_payments = []
    for split in splits:
        if split.expense.paid_by == user:
            outgoing_payments.append(split)
    context['outgoing_payments'] = outgoing_payments
    return render(request, 'see_friend_transanctions.html', context)