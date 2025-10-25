from datetime import datetime, timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from gasapp.serializer import *
from gasapp.forms import *
from gasapp.models import *

# Create your views here.
class Logginpage(View):
    def get(self,request):
        return render(request,'loginpage.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        try:
            obj = LoginTable.objects.get(username=username, password=password)
            request.session['user_id'] = obj.id
            
            # Handle based on user type
            if obj.user_type == 'agency':
                return HttpResponse('''<script>alert("Welcome back");window.location='/Home'</script>''')
            elif obj.user_type =='admin':
                 return HttpResponse('''<script>alert("Welcome back");window.location='/Adminhome'</script>''')
            else:
            
                return HttpResponse('''<script>alert("User not found");window.location='/'</script>''')

        except LoginTable.DoesNotExist:
            # Handle case where login details do not exist
            return HttpResponse('''<script>alert("Invalid username or password");window.location='/'</script>''')
class Home(View):
    def get(self,request):
        return render(request,'Agency/Home.html')   
class Adminhome(View):
    def get(self,request):
        return render (request,'Administration/adminhome.html')    
class agencyview(View):
    def get(self,request):
        agency=AgencyTable.objects.all()
        return render(request,'Administration/viewagency.html',{'agencydata':agency})    
class viewusersbyadmin(View):
 def get(self,request):
    usersss=UserTable.objects.all()
    return render(request,'Administration/userss.html',{'users':usersss})    
class  addsafetyteam(View):
    def get(self,request):
      return render(request,'Administration/addsafety.html')
    
    def post(self, request):
        # Handle form submission on POST request
        form = SafetyRegistrationForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            login_obj = LoginTable.objects.create(
                username=request.POST['username'],
                password=request.POST['password'],
                user_type='safety'
            )
            f.LOGINID = login_obj
            f.save()
            return HttpResponse('''<script>alert("Registration Successful");window.location='/'</script>''')
        else:
            return render(request, 'Administration/addsafety.html.html', {'form': form})
class Users(View):
    def get(self,request):
        users = UserTable.objects.all()
        print(users)
        return render(request,'Agency/users.html',{'users': users})
class delete_user(View):    
 def delete_user(request, id):
    user = get_object_or_404(LoginTable, id=id)
    user.delete()
    return HttpResponse('''<script>alert("Invalid username or password");window.location='/Usersript>''')
   
class Complaints(View):
    def get(self, request):
        complaints = ComplaintTable.objects.all()
        return render(request, 'Administration/complaints.html', {'complaints': complaints})
class CompReply(View):
    def post(self, request, complaint_id):
        reply = request.POST.get('replay')
        complaint = get_object_or_404(ComplaintTable, id=complaint_id)
        complaint.replay = reply
        complaint.save()
        return HttpResponse('''<script>alert("Replay send");window.location='/Usersript>''')
class Viewfiresafety(View):
    def get(self,request):
        safety=fireandsafety.objects.all()
        return render(request,'Administration/viewfireandsafety.html',{'safetys':safety})    

class delete_safetyteam(View):
 def get(self,request, id):
    safety =LoginTable.objects.get(id=id)
    safety.delete()
    return HttpResponse('''<script>alert("Deleted Successfully");window.location='/Adminhome'</script>''')
class Addagency(View):
    def get(self, request):
        return render(request,'Agency/addagency.html')

    def post(self, request):
        # Handle form submission on POST request
        form = AgencyRegistrationForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            login_obj = LoginTable.objects.create(
                username=request.POST['username'],
                password=request.POST['password'],
                user_type='agency'
            )
            f.LOGINID = login_obj
            f.save()
            return HttpResponse('''<script>alert("Registration Successful");window.location='/'</script>''')
        else:
            return render(request, 'agency_registration.html', {'form': form})
class ViewProfiles(View):
    def get(self, request):
        login_id = request.session.get('user_id')
        print('Logged-in user ID:', login_id)
        
        if not login_id:
            return render(request, 'error.html', {'message': 'User not logged in.'})
        
        # Get all agencies linked to this login
        agencies = AgencyTable.objects.filter(LOGINID__id=login_id)
        print('/////////////////')
        print( agencies)
        print('/////////////////')
        
        return render(request, 'Agency/profile.html', {'agency': agencies})
class Emergency(View):
    def get(self, request):
        # Fetch all notifications sorted by latest
        emergency_list = Notification.objects.all().order_by('-date')

        # Fetch latest unviewed notification for popup
        latest_unviewed = Notification.objects.filter(viewed=False).order_by('-date').first()

        # Create a combined list with user info
        combined_data = []
        for e in emergency_list:
            # Try to find a user with matching device_id
            user = UserTable.objects.filter(device_id=e.deviceid).first()
            combined_data.append({
                'name': user.name if user else 'Unknown',
                'place': user.place if user else 'Unknown',
                'consumernumber': user.consumernumber if user else 'N/A',
                'date': e.date,
                'message': e.message,
                'deviceid': e.deviceid,
                'viewed': e.viewed,
            })

        return render(request, 'Agency/viewemergency.html', {
            'emergency': combined_data,
            'latest_unviewed': latest_unviewed
        })

    def post(self, request):
        # Mark latest unviewed as viewed
        latest_unviewed = Notification.objects.filter(viewed=False).order_by('-date').first()
        if latest_unviewed:
            latest_unviewed.viewed = True
            latest_unviewed.save()
        return HttpResponse('''<script>alert("Registration Successful");window.location='/Emergency'</script>''')
class logout(View):
    def get(self,request):
        return render(request,'loginpage.html')   


    
    # ///////////////   API//////////////////////

class UserRegApi(APIView):
    def post(self, request):
        print("#########", request.data)
        user_serial = UserSerializer(data=request.data)
        login_serial = LoginSerializer(data=request.data)

        data_valid = user_serial.is_valid()
        login_valid = login_serial.is_valid()

        if data_valid and login_valid:
            print("&&&&&&&&&&&&&&&")
            password = request.data['password']
            login_profile = login_serial.save(user_type='user', password=password)
            user_serial.save(LOGINID=login_profile)  # ✅ Corrected field name
            return Response(user_serial.data, status=status.HTTP_201_CREATED)

        return Response({
            'login_error': login_serial.errors if not login_valid else None,
            'user_error': user_serial.errors if not data_valid else None
        }, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        print("---------------->")
        response_dict = {}
        print("------------>", request.data)
      # Get data from the request
        username = request.data.get("username")
        password = request.data.get("password")
        # Validate input
        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)
        # Fetch the user from LoginTable
        t_user = LoginTable.objects.filter(username=username,password=password).first()
        print("-------------->", t_user)
        if not t_user:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_401_UNAUTHORIZED)
     
        response_dict["message"] = "success"
        response_dict["login_id"] = t_user.id
        response_dict["user_type"] = t_user.user_type

        return Response(response_dict, status=status.HTTP_200_OK)
class LoginPage(APIView):
    def post(self, request):
        print("##############################")
        response_dict = {}

        username = request.data.get("username")
        password = request.data.get("password")
        print("$$$$$$$$$$$$$$$$$", username)
        print("$$$$$$$$$$$$$$$$$", password)

        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)

        t_user = LoginTable.objects.filter(username=username).first()
        print("xxxxxxxxxxxxxxxxxxxx", t_user)

        if not t_user:
            response_dict["message"] = "Invalid user"
            return Response(response_dict, status=status.HTTP_401_UNAUTHORIZED)

        if t_user.user_type in ["user", "safety"]:
            response_dict["message"] = "success"
            response_dict["login_id"] = t_user.id
            response_dict["user_type"] = t_user.user_type
            return Response(response_dict, status=status.HTTP_200_OK)
        else:
            response_dict["message"] = "Unauthorized user type"
            return Response(response_dict, status=status.HTTP_401_UNAUTHORIZED)
        
class complaint(APIView):
    def get(self, request, id):
        complaints = ComplaintTable.objects.filter(USER__LOGINID_id=id)
        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Add a new complaint for a user
    def post(self, request, id):
        try:
            member = UserTable.objects.get(LOGINID_id=id)
        except UserTable.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ComplaintSerializer(data=request.data)
        print('-------->', request.data)
        if serializer.is_valid():
            serializer.save(USER=member)  # Should match your model field name: USER
            return Response({'message': 'Complaint sent successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class view_notifications(APIView):
    def get(self, request, id):
        try:
            # Step 1: Get user based on login ID
            user = UserTable.objects.get(LOGINID__id=id)

            # Step 2: Fetch all notifications for that device, latest first
            notifications = Notification.objects.filter(deviceid=user.device_id).order_by('-date')

            if not notifications.exists():
                return Response({"message": "No notifications found"}, status=status.HTTP_404_NOT_FOUND)

            # Step 3: Get the latest one
            latest_notification = notifications.first()

            # Step 4: Delete all previous ones except the latest
            notifications.exclude(id=latest_notification.id).delete()

            # Step 5: Serialize only the latest one
            serializer = NotificationSerializer(latest_notification)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserTable.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
class view_profile(APIView):
    def get(self, request, id):
        try:

            # Step 1: Get user based on login ID
            user = UserTable.objects.get(LOGINID__id=id)
            print('***************')
            print(user)
            print('***************')

            # Step 2: Match device ID from user to Notification table
        # Step 3: Serialize notifications
            serializer = ProfileSerializer(user)

            # Step 4: Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except UserTable.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
class cylinder_status(APIView):
     def get(self, request, id):
        try:

            # Step 1: Get user based on login ID
            user = UserTable.objects.get(LOGINID__id=id)
            print('***************')
            print(user)
            print('***************')

            # Step 2: Match device ID from user to Notification table
            notificationss = GasDetails.objects.filter(device_id=user.device_id).order_by('-timestamp')


            # Step 3: Serialize notifications
            serializer = GasDetailsSerializer(notificationss, many=True)

            # Step 4: Return response
            print('-----@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@----->', serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except UserTable.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ViewEmergencyNotifications(APIView):
    def get(self, request):
        try:
            # Fetch all notifications sorted by latest
            emergency_list = Notification.objects.all().order_by('-date')
            print('****************')
            print(emergency_list)
            print('****************')

            # Serialize data with user info included
            serializer = NotificationSerializer(emergency_list, many=True)

            # Fetch latest unviewed notification
            latest_unviewed = Notification.objects.filter(viewed=False).order_by('-date').first()
            latest_data = NotificationSerializer(latest_unviewed).data if latest_unviewed else None

            # Return combined response
            return Response({
                "notifications": serializer.data,
                "latest_unviewed": latest_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class SendNotificationtouserAPIView(APIView):
    def post(self, request):
        consumer_number = request.data.get("consumerNumber")
        print(consumer_number)
        message = request.data.get("message")
        print(message)
        message = request.data.get("message")

        if not consumer_number or not message:
            return Response({"error": "consumerNumber and message are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = UserTable.objects.filter(consumernumber=consumer_number).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        notification = notificationbysafety.objects.create(
            consumernumber=user.consumernumber,
            message=message,
        )

        serializer = NotificationBySafetySerializer(notification)
        return Response({
            "message": "Notification sent successfully",
            "notification": serializer.data
        }, status=status.HTTP_200_OK)
    
class ViewNotificationsFromSafety(APIView):
    def get(self,request):

     notifications = notificationbysafety.objects.all().order_by('-date')  # latest first
     serializer = NotificationsSerializer(notifications, many=True)
     return Response(serializer.data)
  
class LogEventAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            print("Received data:", data)

            device_id = data.get('id')
            event = data.get('event', 'unknown')
            gas_value = data.get('gas_value')
            fan_status = data.get('fan_status', 0)
            light_status = data.get('light_status', 0)
            servo_position = data.get('servo_position', 'open')

            if device_id is None:
                return Response({"status": "error", "message": "Device ID is required"},
                                status=status.HTTP_400_BAD_REQUEST)

            # ✅ Create new gas entry
            gas_entry = GasDetails.objects.create(
                device_id=device_id,
                event=event,
                gas_value=gas_value,
                fan_status=fan_status,
                light_status=light_status,
                servo_position=servo_position
            )
            print('44444444444444444')

            # ✅ Keep only last 5 entries, delete older ones
            total_entries = GasDetails.objects.count()
            if total_entries > 5:
                excess = total_entries - 5
                # Delete oldest records first
                oldest_entries = GasDetails.objects.order_by('timestamp')[:excess]
                GasDetails.objects.filter(id__in=[entry.id for entry in oldest_entries]).delete()
                print(f"Deleted {excess} old entries, keeping last 5.")

            # ✅ Create notification only if gas is high
            if gas_value is not None and gas_value > 4000:
                print('&&&&&&&&&&&&&&&&&&&&&&&&77')
                Notification.objects.create(
                    date=datetime.now(),
                    message="Gas leakage detected",
                    deviceid=device_id,
                    viewed=False
                )
            print('88888888888888888888888')

            return Response({
                "status": "success",
                "device_id": device_id,
                "event": event,
                "gas_value": gas_value,
                "fan_status": fan_status,
                "light_status": light_status,
                "servo_position": servo_position
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)