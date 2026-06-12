from django import http
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from .forms import RegisterForm, LoginForm
from .models import User
from django.http import HttpResponse



class sample(View):

    def get(self, request):
        return HttpResponse("Sample view called")
    
class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:sample')
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                full_name=form.cleaned_data['full_name'],
                phone_number=form.cleaned_data.get('phone_number'),
                password=form.cleaned_data['password']
            )
            login(request, user)
            messages.success(request, f'Welcome {user.full_name}!')
            return redirect('/')
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    print("login view called")
    def get(self, request):
        print("login view called")
        if request.user.is_authenticated:
            return redirect('accounts:sample')
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Email ya password galat hai')
        return render(request, 'accounts/login.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, 'Aap logout ho gaye')
        return redirect('accounts:login')
    

