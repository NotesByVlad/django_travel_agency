from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.views import View
from accounts.models import CustomUser

class ActivateAccountView(View):
    def get(self, request, uid, token):
        try:
            # Decode the UID and get the user
            uid = urlsafe_base64_decode(uid).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # If the token is valid, activate the user
            user.is_active = True
            user.save()
            return render(request, 'accounts/activation/activation_success.html')
        else:
            # Invalid or expired token
            return render(request, 'accounts/activation/activation_invalid.html')