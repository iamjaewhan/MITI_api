from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    use_for_related_fields = True
    
    def create_user(self, email, username, password, password_check):
        if not email:
            raise ValueError('올바르지 않은 입력입니다.')
        if not username:
            raise ValueError('올바르지 않은 입력입니다.')
        if not password:
            raise ValueError('올바르지 않은 입력입니다.')
        if password == password_check:
            user = self.model(email=self.normalize_email(email), username=username)
            user.set_password(password)
            user.save()
            return user
        else:
            raise ValueError('올바르지 않은 입력입니다.')
    
    def create_superuser(self, email, password):
        user = self.create_user(email=email, username=username, password=password, password_check=password_check)
        user.is_staff = True
        user.save()
        return user
    
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    

class AllUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    

class DeletedUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=False)
    

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, null=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    USERNAME_FIELD = 'email'
    
    objects = UserManager()
    all_objects = AllUserManager()
    deleted_objects = DeletedUserManager()
    
    def __str__(self):
        return self.email

    def is_admin(self):
        return self.is_staff
    
    def has_perm(self, perm, obj=None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return self.is_staff
    
    @property
    def user(self):
        return self.email
        