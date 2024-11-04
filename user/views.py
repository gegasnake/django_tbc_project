from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm, CustomLoginForm


class RegistrationView(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Registration successful. Please log in.')
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid credentials')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")

        return super().dispatch(request, *args, **kwargs)
