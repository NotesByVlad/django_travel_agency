from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.views import View
from accounts.models import CustomUser
from django.contrib import messages
from django.shortcuts import redirect

class ActivateAccountView(View):
    def get(self, request, uid, token):
        try:
            # Decode the UID and get the user
            uid = urlsafe_base64_decode(uid).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid or has expired.")
            return redirect('register')