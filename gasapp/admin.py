from django.contrib import admin

from gasapp.models import AgencyTable, ComplaintTable, GasDetails, LoginTable, Notification, UserTable, fireandsafety, notificationbysafety

# Register your models here.
admin.site.register(LoginTable)
admin.site.register(AgencyTable)
admin.site.register(UserTable)
admin.site.register(Notification)
admin.site.register(ComplaintTable)

admin.site.register(GasDetails)
admin.site.register(fireandsafety)
admin.site.register(notificationbysafety)


