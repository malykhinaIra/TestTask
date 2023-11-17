from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages


from .forms import CustomUserCreationForm, CustomUserEditForm, CustomPasswordChangeForm
from .models import CustomUser


class LoginInterfaceView(LoginView):
    template_name = 'sign_in.html'
    next_page = '/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('site_list')
        return super().get(request, *args, **kwargs)
    

class LogoutInterfaceView(LogoutView):
    next_page = '/'


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('site_list')
        return super().get(request, *args, **kwargs)
    

class ProfileView(UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, **kwargs):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been successfully updated.')
        return super().form_valid(form)
    

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('users:profile')
    template_name = 'change_password.html'
