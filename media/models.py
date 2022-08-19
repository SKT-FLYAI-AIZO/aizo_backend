from django.db import models
from account import models as account_model


class Video(models.Model):
    email = models.ForeignKey(account_model.Account, related_name="account", on_delete=models.CASCADE, db_column="email")
    date = models.CharField(max_length=20)
    location = models.CharField(max_length=45, blank=True)
    path = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'video'
