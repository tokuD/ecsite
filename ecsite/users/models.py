from django.db import models
from django.contrib.auth.models import PermissionMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager

class User(AbstractBaseUser, PermissionMixin):
    """カスタムユーザーモデル"""
    initial_point = 50000
    email = models.PositiveIntegerField(default=initial_point)
    is_staff = models.BooleanField("is_staff", default=False)
    is_active = models.BooleanField("is_active", default=True)
    date_joined = models.DateTimeField("date_joined", default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELD = []
    
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        
class UserManager(BaseUserManager):
    """カスタムユーザーマネージャー"""
    
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        # emailを必須にする
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalized_email(email)
        #emailを使ってUserデータを作成
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)