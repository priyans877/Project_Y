from django.db import models

# Create your models here.

class chart_data(models.Model):
    student_name = models.CharField(max_length = 100 )
    roll_no = models.CharField(max_length = 15)
    semester = models.CharField(max_length=70)
    branch = models.CharField(max_length=70)
    year = models.CharField(max_length=10)
    cgpa = models.FloatField(max_length = 10 , null = True , blank = True)
    recount = models.IntegerField(null =True)
    
    def Meta(self):
        return  f"{self.student_name}_{self.roll_no}"
    
    