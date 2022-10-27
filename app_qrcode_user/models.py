from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser,UserManager
)
from django.dispatch import receiver
from django.db.models.signals import post_save


class MyUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomerUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)

class CustomerUser(AbstractUser):
    USER_TYPE = ((1, "Admin"), (2, "Agent"), (3, "Enseignant") ,(4, "Etudiant"))
    GENDER = [("M", "Masculin"), ("F", "Feminin")]

    username = None  # Removed username, using email instead
    nom = models.CharField(max_length=20)
    postnom = models.CharField(max_length=20)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    profile_image = models.ImageField(upload_to='profile/')
    user_type = models.CharField(default=1, max_length=1)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def __str__(self):
        return self.email



class ClientUser(models.Model):
    admin = models.OneToOneField(CustomerUser, on_delete=models.CASCADE)


@receiver(post_save, sender=CustomerUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            ClientUser.objects.create(admin=instance)
       


@receiver(post_save, sender=CustomerUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.type_user == 1:
        instance.admin.save()
   