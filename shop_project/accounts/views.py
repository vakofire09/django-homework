from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import UserRegisterForm, ProfileForm
from .models import Profile
from django.contrib.auth import logout


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        profile_form = ProfileForm(self.request.POST, instance=self.object.profile)
        if profile_form.is_valid():
            profile_form.save()
        return response


class UserLoginView(LoginView):
    template_name = 'accounts/login.html' 
    next_page = reverse_lazy('home')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home') 



class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile
