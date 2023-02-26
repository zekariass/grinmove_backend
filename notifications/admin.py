from django.contrib import admin
from notifications import models as notif_models

admin.site.register(notif_models.NotificationChannel)
admin.site.register(notif_models.NotifChannelSetting)
admin.site.register(notif_models.NotificationTemplate)
admin.site.register(notif_models.NotificationTrigger)
admin.site.register(notif_models.NotifTriggerSetting)
admin.site.register(notif_models.NotifTargetType)
admin.site.register(notif_models.Notification)
admin.site.register(notif_models.UserNotification)