from django.shortcuts import render

from .models import tweet
from .forms import TweetForm, UserRegistrationForm, ProfileForm
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
   tweets = tweet.objects.all().order_by('-created_at')

   return render(request,'tweet_list.html',{'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method=="POST":
        form = TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user= request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TweetForm()
    return render(request,'tweet_form.html',{'form': form})
@login_required
def tweet_edit(request, tweet_id):
    tweet_obj = get_object_or_404(tweet, pk=tweet_id, user=request.user)

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet_obj)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet_obj)

    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet_obj = get_object_or_404(tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        tweet_obj.delete()
        return redirect('tweet_list')

    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet_obj})

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)  

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('login') 
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



def tweet_list(request):
    query = request.GET.get('q')
    if query:
        tweets = tweet.objects.filter(
            Q(text__icontains=query) | Q(user__username__icontains=query)
        ).order_by('-created_at')
    else:
        tweets = tweet.objects.all().order_by('-created_at')

    return render(request, 'tweet_list.html', {'tweets': tweets, 'query': query})

def profile_view(request):
    tweets = tweet.objects.filter(user=request.user).order_by('-created_at')

    context = {
        "tweets": tweets,
    }
    return render(request, 'registration/profile.html', context)