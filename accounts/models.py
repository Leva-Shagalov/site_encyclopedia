from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    avatar = models.FileField(upload_to="avatars/", blank=True,)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "профиль пользователя"
        verbose_name_plural = "профили пользователей"