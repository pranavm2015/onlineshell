from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class user(models.Model):
    uid = models.IntegerField(null=True)
    email = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "user";
	