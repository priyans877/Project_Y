from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
# Create your models here.



class excle_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    file = models.FileField(upload_to='excel_files/')
    semester = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    
    def __str__(self):
        return "{self.branch}_{self.year}_{self.semester}".format(self=self)
    
    def filesize(self):
        x = self.file.size
        y = 512000
        if x < y:
            value = round(x/1000, 2)
            ext = ' kb'
        elif x < y*1000:
            value = round(x/1000000, 2)
            ext = ' Mb'
        else:
            value = round(x/1000000000, 2)
            ext = ' Gb'
        return str(value)+ext
    

class excle_model2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    retieve_data = JSONField()
    semester = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    
    def __str__(self):
        return "{self.branch}_{self.year}_{self.semester}".format(self=self)