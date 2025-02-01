from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User

# Create your models here.


class EmployeeProfile(BaseModel):
    employee=models.OneToOneField(User,on_delete=models.CASCADE,related_name="employee_profile")
    name= models.CharField(max_length=20)
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100,null=True,blank=True)
    job_title= models.CharField(max_length=50)
    salary= models.IntegerField()
    profile_image=models.ImageField(upload_to='employee_profile')


    
    def __str__(self):
        return f"{self.name} - salary->{self.salary}"
    