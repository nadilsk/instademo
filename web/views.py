from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from . models import UserData,Post, Comment, Like
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def user_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(request.POST)
        user = User()
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.set_password(password)
        user.save()

        data = UserData()
        data.phone = phone
        data.age = age
        data.gender = gender
        data.user = user
        data.save()
        print(user, 'user---')
        print(data, 'data---')

        return redirect('/login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
        return redirect('/home/')
    return render(request, 'login.html')

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')

@login_required(login_url='/login/')
def home(request):
    posts = Post.objects.filter(
        is_deleted=False,
        is_blocked=False
    ).order_by('-id')

    for post in posts:
        post.comment_list = Comment.objects.filter(
            post=post,
            is_blocked=False
        )

        post.like_count = Like.objects.filter(
            post=post
        ).count()

        post.is_liked = Like.objects.filter(
            post=post,
            user=request.user
        ).exists()

    return render(request, 'home.html', {
        'posts': posts
    })


@login_required(login_url='/login/')
def add_post(request):
    if request.method=='POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_image = request.POST.get('is_image')
        user=request.user

        post = Post()
        post.title = title
        post.description = description
        post.is_image = is_image
        if is_image == 'True':
            post.image = request.FILES.get('image')
        else:  
            post.video = request.FILES.get('video')
        post.user = user
        post.save()
        return redirect('/home')
    return render(request, 'add-post.html')

@login_required(login_url='/login/')
def add_comment(request, id):

    if request.method == 'POST':

        text = request.POST.get('comment')
        post = get_object_or_404(Post, id=id)
        user = request.user

        comment = Comment()
        comment.comment = text
        comment.post = post
        comment.user = user
        comment.save()

    return redirect('/home/')

def like_post(request, id):

    post = get_object_or_404(Post, id=id)

    like = Like.objects.filter(post=post, user=request.user)

    if like.exists():
        like.delete()
    else:
        Like.objects.create(post=post, user=request.user)

    return redirect('home')