from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
