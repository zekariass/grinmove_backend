from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.utils import timezone


class MyHomeUserGroup(models.Model):
    """
    User group
    """
    name = models.CharField(verbose_name='user group', max_length=50, blank=False, unique=True)
    description = models.TextField()


class MyHomeUserManager(BaseUserManager):
    """
    User manager for the custom user model
    """
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_blocked', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('is_admin must be True for superuser')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be True for superuser')

        return self.create_user(email, first_name, last_name, password, **extra_fields)

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError('You must provide email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user
        

class MyHomeUser(AbstractBaseUser):
    """
    Custom user model which replaces built is User model
    """
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(verbose_name='email address', unique=True, blank=False, null=False)
    user_group = models.ForeignKey(MyHomeUserGroup, related_name='users', related_query_name='user',
                                     null=True, blank=False, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(editable=False, null=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)

    objects = MyHomeUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return '%s %s %s' % (self.first_name, self.last_name, self.email)

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        '''Check if the user has specific permission'''
        return True
    
    def has_module_perms(self, app_label):
        '''Check if the user has module level permission'''
        return True


class LoginHistory(models.Model):
    """
    This class allows to track the login history of users. Every time a user logs in to the 
    system new record is added to this table
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="login_historys")
    logged_in_on = models.DateTimeField(default=timezone.now, editable=False)
    logged_out_on = models.DateTimeField(default=timezone.now, editable=False, null=True)

    @property
    def is_logged_in(self):
        if self.logged_in_on is not None and self.logged_out_on is None:
            return True


class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    permission = models.ManyToManyField(Permission, verbose_name="permissions in this role")

    def __str__(self):
        return self.name


class SystemAdminGroup(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    role = models.ManyToManyField(Role, verbose_name="roles in this group", related_name="roles")

    def __str__(self):
        return self.name


class SystemAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="parent user")
    admin_group = models.OneToOneField(SystemAdminGroup, on_delete=models.CASCADE)
    second_password = models.CharField(verbose_name="Second password of the admin", max_length=30, null=True, blank=True)
    use_sec_pass_for_login = models.BooleanField(verbose_name="use second password for login?", default=True)

    def __str__(self):
        return self.user.first_name