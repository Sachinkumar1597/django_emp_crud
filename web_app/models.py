from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Records(models.Model):
    creation_date=models.DateTimeField(auto_now_add=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone_no=models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', message="Phone number must be 10 digits")])
    email=models.EmailField(max_length=50)
    address=models.CharField(max_length=250)
    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)

    def __str__(self):
        return self.first_name+"  "+self.last_name
    