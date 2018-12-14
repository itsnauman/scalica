from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Following, Post, FollowingForm, PostForm, MyUserCreationForm

# imports for rpc client calls
import grpc
from hashtag_pb2 import *
from hashtag_pb2_grpc import *

# Anonymous views
#################
def index(request):
  if request.user.is_authenticated():
    return home(request)
  else:
    return anon_home(request)

def anon_home(request):
  return render(request, 'micro/public.html')

def stream(request, user_id):  
  # See if to present a 'follow' button
  form = None
  if request.user.is_authenticated() and request.user.id != int(user_id):
    try:
      f = Following.objects.get(follower_id=request.user.id,
                                followee_id=user_id)
    except Following.DoesNotExist:
      form = FollowingForm
  user = User.objects.get(pk=user_id)
  post_list = Post.objects.filter(user_id=user_id).order_by('-pub_date')
  paginator = Paginator(post_list, 10)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    posts = paginator.page(1) 
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    posts = paginator.page(paginator.num_pages)
  context = {
    'posts' : posts,
    'stream_user' : user,
    'form' : form,
  }
  return render(request, 'micro/stream.html', context)



def register(request):
  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    new_user = form.save(commit=True)
    # Log in that user.
    user = authenticate(username=new_user.username,
                        password=form.clean_password2())
    if user is not None:
      login(request, user)
    else:
      raise Exception
    return home(request)
  else:
    form = MyUserCreationForm
  return render(request, 'micro/register.html', {'form' : form})


def stream_hashtag_with_sentiment(request, hashtag):
    # get the hashtag from the request
    # send an rpc call to get all the tweet ids and the sentiment 
    # associated with the hashtag
    # render all the tweets
    # print "THE HASHTAG IS " + hashtag
    # check of the hashtag has the character '#' and format it the way redis takes it
    #  hashtag = request.GET.get('hashtag')
    if hashtag[0] != '#':
      hashtag = '#' + hashtag
    tweet_ids = []
    sentiment = None
    with grpc.insecure_channel('35.185.58.180:50051') as channel:
      stub = HashtagsStub(channel)
      response = stub.getTweetsByHashtag(TweetHashtagRequest(hashtag=hashtag))
      tweet_ids = response.tweets
      res = stub.getTweetSentiment(TweetHashtagRequest(hashtag=hashtag))
      #sentiment = "temp"
      print "the sentiment is: " + res.sentiment 

    # get all the tweets from datbase and render
    tweet_list = Post.objects.filter(id__in=tweet_ids) # may need to cast tweet_ids to python list
    
    # pagination
    paginator = Paginator(tweet_list, 5)
    page = request.GET.get('page')
    try:
      tweets = paginator.page(page)
    except PageNotAnInteger:
      tweets = paginator.page(1)
    except EmptyPage:
      tweets = paginator.get_page(paginator.num_pages)
    print "the sentiment for "+ hashtag + " is  "+ res.sentiment  
    return render(request, 'micro/hashtag_search_with_sentiment.html', {'posts': tweets, 'sentiment': res.sentiment, 'hashtag': hashtag})


# Authenticated views
#####################
@login_required
def home(request):
  '''List of recent posts by people I follow'''
  try:
    my_post = Post.objects.filter(user=request.user).order_by('-pub_date')[0]
  except IndexError:
    my_post = None
  follows = [o.followee_id for o in Following.objects.filter(
    follower_id=request.user.id)]
  post_list = Post.objects.filter(
      user_id__in=follows).order_by('-pub_date')[0:10]
  context = {
    'post_list': post_list,
    'my_post' : my_post,
    'post_form' : PostForm,
    'hashtag_error': 'Field cannot be empty'
  }
  return render(request, 'micro/home.html', context)

# Allows to post something and shows my most recent posts.
@login_required
def post(request):
  if request.method == 'POST':
    form = PostForm(request.POST)
    new_post = form.save(commit=False)
    new_post.user = request.user
    new_post.pub_date = timezone.now()
    new_post.save()
    # get the post id
    # make an rpc call to send the tweet id and the text
    post_id = new_post.id
    text = new_post.text
    channel = grpc.insecure_channel('35.185.58.180:50051')
    stub = HashtagsStub(channel)
    stub.sendTweet(TweetRequest(tweet=text, tweet_id=post_id))
    channel.close()    
    return home(request)
  else:
    form = PostForm
  return render(request, 'micro/post.html', {'form' : form})

@login_required
def follow(request):
  if request.method == 'POST':
    form = FollowingForm(request.POST)
    new_follow = form.save(commit=False)
    new_follow.follower = request.user
    new_follow.follow_date = timezone.now()
    new_follow.save()
    return home(request)
  else:
    form = FollowingForm
  return render(request, 'micro/follow.html', {'form' : form})



    




