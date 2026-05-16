from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models



class UserManager(BaseUserManager):
    def create_user(self, username, email, password = None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username  is required')
        
        email = self.normalize_email(email)

        user = self.model(
            username = username, 
            email = email, 
            **extra_fields
        )

        user.set_password(password)

        user.save(using = self._db)

        return user
    
    def create_superuser(self, username, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            username, 
            email, 
            password, 
            **extra_fields
        )
    

class User(AbstractUser):
    # As abstractUser already includes 'username', we just need to add 'email', 'is_merchant' and 'date_joined'
    email = models.EmailField(unique = True)
    is_merchant = models.BooleanField(default = False)
    date_joined = models.DateTimeField(auto_now_add = True)

    objects = UserManager()

    def __str__(self):
        return self.username