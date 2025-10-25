"""
URL configuration for Gasleakage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from gasapp.views import *

urlpatterns = [
    path('',Logginpage.as_view(),name='Logginpage'),
    path('Home',Home.as_view(),name='Home'),
    path('Users',Users.as_view(),name='Users'),
    path('delete-user/<int:id>/',delete_user.as_view(), name='delete_user'),
    path('Complaints', Complaints.as_view(), name='Complaints'),
    path('CompReply/<int:complaint_id>',CompReply.as_view(),name='CompReply'),
    path('Addagency',Addagency.as_view(),name='Addagency'),
    path('ViewProfiles',ViewProfiles.as_view(),name='ViewProfiles'),
    path('Adminhome',Adminhome.as_view(),name='Adminhome'),
    path('agencyview',agencyview.as_view(),name='agencyview'),
    path('viewusersbyadmin',viewusersbyadmin.as_view(),name='viewusersbyadmin'),
    path('Viewfiresafety',Viewfiresafety.as_view(),name='Viewfiresafety'),
    path('addsafetyteam',addsafetyteam.as_view(),name='addsafetyteam'),
    path('delete_safetyteam/<int:id>/', delete_safetyteam.as_view(), name='delete_safetyteam'),
    path('Emergency',Emergency.as_view(),name='Emergency'),
    path('logout',logout.as_view(),name='logout'),


    # ////////////// API URLS /////////////////////
    path('UserRegApi/',UserRegApi.as_view(),name='UserRegApi'),
    path('login/',LoginPage.as_view(), name='login'),
    path('view_notifications/<int:id>',view_notifications.as_view(),name='view_notifications'),
    path('view_profile/<int:id>',view_profile.as_view(),name='view_profile'),
    path('complaint/<int:id>',complaint.as_view(),name='complaint'),
    path('cylinder_status/<int:id>',cylinder_status.as_view(),name='cylinder_status'),
    path('ViewEmergencyNotifications/', ViewEmergencyNotifications.as_view(), name='ViewEmergencyNotifications'),
    path('SendNotificationtouserAPIView/',SendNotificationtouserAPIView.as_view(),name='SendNotificationtouserAPIView'),
    path('view_notificationsfromsafety/', ViewNotificationsFromSafety.as_view(), name='view_notificationsfromsafety'),

    ##########################Embedded#####################################33
    path('log_event',LogEventAPIView.as_view(), name='log_event'),

]
