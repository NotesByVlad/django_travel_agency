
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
from accounts.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render
from django.core.mail import send_mail


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/auth/login_register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'register'
        context['register_form'] = CustomUserCreationForm()
        context['login_form'] = AuthenticationForm()
        return context
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Don't log them in yet
        user.save()

        # Prepare email verification
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        message = render_to_string('accounts/activation/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return render(self.request, 'accounts/activation/check_your_email.html')