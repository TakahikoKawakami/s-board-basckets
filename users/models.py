from django.db import models

# Create your models here.
class Accounts(models.Model):
    """アカウント"""
    name = models.CharField('ユーザ名', max_length=255)
    email = models.CharField('メールアドレス', max_length=255)

    def __str__(self):
        return self.name