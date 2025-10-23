from django.db import models

# Create your models here.
class LoginTable(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50, null=True, blank=True)  
class AgencyTable(models.Model):
    Agencyname=models.CharField(max_length=100,null=True,blank=True)    
    Phone=models.IntegerField(null=True,blank=True)
    place=models.CharField(null=True,blank=True)
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True) 
class fireandsafety(models.Model):
    Phone=models.IntegerField(null=True,blank=True)
    place=models.CharField(null=True,blank=True)
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True) 
        
class UserTable(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    phone=models.IntegerField(null=True,blank=True)
    place=models.CharField(max_length=100,null=True,blank=True)
    consumernumber=models.CharField(max_length=100,null=True,blank=True)
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    device_id=models.IntegerField(null=True,blank=True)
class Notification(models.Model):
    date=models.DateTimeField(null=True,blank=True)
    message=models.CharField(max_length=100,null=True,blank=True)
    deviceid=models.IntegerField(null=True,blank=True)
    viewed = models.BooleanField(default=False)
class ComplaintTable(models.Model):
    USER=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    Complaint=models.CharField(max_length=100,null=True,blank=True)
    date=models.DateField(auto_now_add=True, null=True,blank=True)
    replay=models.CharField(max_length=100,null=True,blank=True, default="pending")

class GasDetails(models.Model):
    timestamp=models.DateTimeField(null=True,blank=True)
    device_id=models.IntegerField(null=True,blank=True)
    event=models.CharField(max_length=100,null=True,blank=True)
    gas_value=models.IntegerField(null=True,blank=True)
    light_status=models.CharField(max_length=100,null=True,blank=True)
    fan_status=models.CharField(max_length=100,null=True,blank=True)
    servo_position=models.CharField(max_length=100,null=True,blank=True)
class notificationbysafety(models.Model):
    message=models.CharField(max_length=100,null=True,blank=True)
    date=models.DateTimeField(auto_now=True,null=True,blank=True)
    consumernumber=models.CharField(max_length=100,null=True,blank=True)






    