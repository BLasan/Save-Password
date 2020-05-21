from django.db import models

# Create your models here.

class Users(models.Model):
    user_name = models.CharField(max_length=100,default="Unknown",null=False)
    user_email = models.CharField(max_length=250,null=False,primary_key=True)
    password = models.CharField(null=False,max_length=100)

    class Meta:
        db_table = "reg_users"
