from gasapp.models import *
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

class LoginSerializer(ModelSerializer):
    class Meta:
        model=LoginTable
        fields=['username','password']

class UserSerializer(ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['id', 'name','phone','place', 'phone', 'consumernumber']
class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintTable
        fields = ['Complaint', 'replay', 'date']     
class NotificationSerializer(ModelSerializer):
    class Meta:
     model=Notification    
     fields=['id', 'date','message','deviceid']    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserTable
        fields = ['id', 'name','phone','place', 'phone', 'consumernumber']
class GasDetailsSerializer(ModelSerializer):
    class Meta:
     model=GasDetails    
     fields=['id', 'timestamp','device_id','event','gas_value','light_status','fan_status','servo_position']   
class NotificationSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()
    consumernumber = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['date', 'message', 'deviceid', 'viewed', 'name', 'place', 'consumernumber']

    def get_name(self, obj):
        user = UserTable.objects.filter(device_id=obj.deviceid).first()
        return user.name if user else "Unknown"

    def get_place(self, obj):
        user = UserTable.objects.filter(device_id=obj.deviceid).first()
        return user.place if user else "Unknown"

    def get_consumernumber(self, obj):
        user = UserTable.objects.filter(device_id=obj.deviceid).first()
        return user.consumernumber if user else "N/A"
class NotificationBySafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = notificationbysafety
        fields = ['id', 'consumernumber', 'message', 'date']
        read_only_fields = ['id', 'date']
class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = notificationbysafety
        fields = ['id', 'date', 'message', ]            

