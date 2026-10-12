from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import RegisterForm, ProfileForm, PostForm, CommentForm
from .models import Profile, Post, Comment, Like, Follow

def ensure_profile(user): Profile.objects.get_or_create(user=user)

def feed(request):
    if request.user.is_authenticated: ensure_profile(request.user)
    query = request.GET.get('q','').strip()
    posts = Post.objects.select_related('author','author__profile').prefetch_related('likes','comments__author')
    if query: posts = posts.filter(Q(text__icontains=query) | Q(author__username__icontains=query))
    return render(request,'social/feed.html',{'posts':posts,'query':query,'post_form':PostForm()})

def register_view(request):
    if request.user.is_authenticated: return redirect('feed')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(); login(request,user); messages.success(request,'Welcome to Loop!'); return redirect('feed')
    return render(request,'social/register.html',{'form':form})

@login_required
@require_POST
def create_post(request):
    ensure_profile(request.user); form = PostForm(request.POST)
    if form.is_valid():
        post=form.save(commit=False); post.author=request.user; post.save(); messages.success(request,'Your post was published.')
    else: messages.error(request,'Please check the post and try again.')
    return redirect(request.META.get('HTTP_REFERER','feed'))

@login_required
@require_POST
def delete_post(request, post_id):
    post=get_object_or_404(Post,pk=post_id)
    if post.author_id != request.user.id: return HttpResponseForbidden('You can only delete your own posts.')
    post.delete(); messages.success(request,'Post deleted.'); return redirect('feed')

@login_required
@require_POST
def add_comment(request, post_id):
    post=get_object_or_404(Post,pk=post_id); text=request.POST.get('text','').strip()
    if text and len(text)<=500: Comment.objects.create(post=post,author=request.user,text=text)
    else: messages.error(request,'Enter a comment under 500 characters.')
    return redirect(request.META.get('HTTP_REFERER','feed'))

@login_required
@require_POST
def toggle_like(request, post_id):
    post=get_object_or_404(Post,pk=post_id); like, created=Like.objects.get_or_create(post=post,user=request.user)
    if not created: like.delete()
    return redirect(request.META.get('HTTP_REFERER','feed'))

@login_required
@require_POST
def toggle_follow(request, username):
    target=get_object_or_404(User,username=username)
    if target == request.user:
        messages.info(request,'You cannot follow yourself.')
    else:
        relation,created=Follow.objects.get_or_create(follower=request.user,following=target)
        if not created: relation.delete()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer) if referer else redirect('profile', username=username)

def profile_view(request, username):
    person=get_object_or_404(User,username=username); ensure_profile(person)
    is_following=request.user.is_authenticated and request.user != person and Follow.objects.filter(follower=request.user,following=person).exists()
    posts=person.posts.select_related('author','author__profile').prefetch_related('likes','comments__author')
    return render(request,'social/profile.html',{'person':person,'posts':posts,'is_following':is_following})

@login_required
def edit_profile(request):
    ensure_profile(request.user); form=ProfileForm(request.POST or None,instance=request.user.profile)
    if request.method=='POST' and form.is_valid():
        form.save(); messages.success(request,'Profile updated.'); return redirect('profile',username=request.user.username)
    return render(request,'social/edit_profile.html',{'form':form})

def people(request):
    if request.user.is_authenticated: ensure_profile(request.user)
    query=request.GET.get('q','').strip(); users=User.objects.select_related('profile').all()
    if request.user.is_authenticated: users=users.exclude(pk=request.user.pk)
    if query: users=users.filter(Q(username__icontains=query)|Q(profile__bio__icontains=query))
    users=users.order_by('username')[:100]
    following_ids=set(Follow.objects.filter(follower=request.user).values_list('following_id',flat=True)) if request.user.is_authenticated else set()
    return render(request,'social/people.html',{'people':users,'query':query,'following_ids':following_ids})
