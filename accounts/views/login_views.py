from django.contrib.auth.views import LoginView
from accounts.forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    template_name = 'accounts/auth/login_register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'login'
        # Add the registration form instance to the context
        context['login_form'] = CustomUserCreationForm()  # Include registration form in the context
        return context