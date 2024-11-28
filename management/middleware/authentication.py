from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0. Exclude those webpages that can be accessed without being logged in
        # 'request.path_info': Get the request URL of the current user 
        # E.g. if you are currently visiting 'http://127.0.0.1:8000/login/', then 'request.path_info' = /login/
        if request.path_info in ["/login/", "/image/random/"]:
            return None
        
        
        # 1. Read the session info of the current visiting user
        user_info_dict = request.session.get("user_info")
        # If the session info CAN be read => User has already signed in => Can pass the request along to the next middleware
        if user_info_dict:
            return 
        # If the session info CANNOT be read => User has NOT signed in => redirect to the login page
        if not user_info_dict:
            return redirect("/login/")
            
        
        
        
    def process_response(self, request, response):
        return response
    