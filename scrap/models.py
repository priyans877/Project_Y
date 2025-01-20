from django.db import models
from django.db.models import JSONField
# Create your models here.

class form_data(models.Model):
    id = models.AutoField(primary_key=True)
    captcha = models.ImageField(upload_to='images/')
    roll_no = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.roll_no}.{self.semester}"
    
class trail_json(models.Model):
    s_name = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=50)
    # re_count = models.IntegerField(max_length = 20)
    result = JSONField()
    
class result(models.Model):
    s_name = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=50)
    f_name = models.CharField(max_length = 75)
    m_name = models.CharField(max_length=50)
    category = models.CharField(max_length = 75)
    sgpa = models.CharField(max_length = 100)
    cgpa =  models.CharField(max_length = 50, blank=True , null = True )
    re_count = models.CharField(max_length=50)
    result_s = JSONField()