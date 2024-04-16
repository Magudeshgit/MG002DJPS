from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    print("AUTH BACKEND")
    userModel = get_user_model()
    def authenticate(self, request, email=None, password=None, **kwargs):
        print("AUTH BACKEND**", email, password)
        if email is None:
            return ValueError("Email field cannot be empty")
        else:
            try:
                user = self.userModel.objects.get(email=email)
                if user.check_password(password):
                    return user
                else:
                    return None
            except ObjectDoesNotExist:
                return None
            

            
