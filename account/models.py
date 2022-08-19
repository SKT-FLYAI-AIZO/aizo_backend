from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=45, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'account'
