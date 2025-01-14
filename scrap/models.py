from django.db import models

# Create your models here.

class form_data(models.Model):
    captcha = models.ImageField(upload_to='images/')
    roll_no = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.roll_no}.{self.semester}"