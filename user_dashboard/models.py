from django.db import models

# Create your models here.

class Credentials(models.Model):
    user_email = models.CharField(max_length=250,null=False,primary_key=True)
    password = models.BinaryField(null=False,max_length=100)
    salt = models.BinaryField(null=False)

    def __str__(self):
        return self.user_email

    class Meta:
        db_table = "credentials"

