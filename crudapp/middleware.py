from django.urls import reverse
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.http import HttpResponseRedirect



class CustomAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        # This is required as a base case otherwise the middleware would loop infinitely
        if request.path == reverse('login') or request.path == reverse('logout'):
            return None
        
        if request.method == 'GET' and not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
