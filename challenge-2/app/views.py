from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Message 

@require_http_methods(['GET', 'POST'])
def log_in(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')
    context = { 'title': 'Login' }
    if request.method == 'GET':
        return render(request, 'form.html', context)
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if username == '':
        context['error'] = 'Username cannot be empty!'
        return render(request, 'form.html', context) 
    if password == '':
        context['error'] = 'Password cannot be empty!'
        return render(request, 'form.html', context)
    user = authenticate(username=username, password=password)
    if not user:
        context['error'] = 'Invalid username and/or password!'
        return render(request, 'form.html', context)
    login(request, user)
    return redirect('home')

@require_http_methods(['GET', 'POST'])
def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')
    context = { 'title': 'Register' }
    if request.method == 'GET':
        return render(request, 'form.html', context)
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if username == '':
        context['error'] = 'Username cannot be empty!'
        return render(request, 'form.html', context) 
    if password == '':
        context['error'] = 'Password cannot be empty!'
        return render(request, 'form.html', context)
    if User.objects.filter(username__exact=username).exists():
        context['error'] = 'Username already exists.'
        return render(request, 'form.html', context) 
    user = User.objects.create_user(username=username, password=password)
    user = authenticate(username=username, password=password)
    if not user:
        context['error'] = 'Error creating user. Try again'
        return render(request, 'form.html', context)
    login(request, user)
    return redirect('home')

@login_required
@require_http_methods(['GET', 'POST'])
def log_out(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('log_in')

@login_required
@require_http_methods(['GET', 'POST'])
def home(request: HttpRequest) -> HttpResponse:
    # Renew csrf token
    get_token(request)
    return render(request, 'index.html', {})

@login_required
@require_http_methods(['POST'])
def query(request: HttpRequest) -> HttpResponse:
    try:
        if User.objects.filter(**request.POST.dict()).exists():
            response = {'found': True}
        else: 
            response = {'found': False}
    except Exception:
        response = JsonResponse({'error': 'Error encountered.'}, status=500)
        response.delete_cookie('csrftoken') # must renew csrf token 
        return response

    response = JsonResponse(response, status=200)
    response.delete_cookie('csrftoken') # must renew csrf token 
    return response

@login_required
@require_http_methods(['GET', 'POST'])
def message(request: HttpRequest) -> HttpResponse:
    context = {}
    context['messages'] = Message.objects.filter(user=request.user).all()
    
    if request.method == 'GET':
        return render(request, 'message.html', context)

    message = request.POST.get('message', '')

    if message == '':
        context['error'] = 'Message cannot be empty!'
        return render(request, 'message.html', context)
    
    Message.objects.create(
        user=request.user,
        text=message
    )

    # Max 5 posts
    if Message.objects.filter(user=request.user).count() > 5:
        oldest = Message.objects.filter(user=request.user).order_by('created_at').first()
        if oldest: 
            oldest.delete()

    context['messages'] = Message.objects.filter(user=request.user).all()
    return render(request, 'message.html', context)
