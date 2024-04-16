from django.contrib.auth.models import AbstractUser, BaseUserManager

class User_Manager(BaseUserManager):
    def create_user(self, email=None,password=None,**extra_fields):
        if not email:
            raise ValueError("Email field should not be empty")
        user = self.model(email = email,)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email=None,password=None,**extra_fields):
        if not email:
            raise ValueError("Email field should not be empty")
        user = self.create_user(email=email,password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user