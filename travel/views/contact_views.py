from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from travel.forms import ContactForm 
from travel.models import ContactMessage



class ContactFormView(SuccessMessageMixin, FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    success_message = "Thank you for your message!"

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['name'] = self.request.user.username
            initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        ContactMessage.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            message=form.cleaned_data['message'],
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_messages'] = ContactMessage.objects.filter(
                user=self.request.user
            ).order_by('-created_at')
        return context