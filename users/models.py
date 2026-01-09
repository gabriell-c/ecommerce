from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    phone = models.CharField(max_length=20, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    avatar = models.ImageField( upload_to="avatars/", blank=True, null=True)
    cep = models.PositiveIntegerField(blank=True, null=True)
    street = models.CharField(max_length=100,blank=True, null=True)
    number = models.PositiveSmallIntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return f"Perfil de {self.user.username}"