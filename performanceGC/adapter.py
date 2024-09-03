from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/profile/{ficha}/"
        return path.format(ficha=request.user.empleado.ficha)
    
    def is_open_for_signup(self, request):
        return False