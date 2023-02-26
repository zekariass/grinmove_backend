from glob import escape
from django.db import models
from django.utils import timezone
from django.conf import settings


"""Users can receive notifications through various channels, such as email, in-app, SMS, etc"""
class NotificationChannel(models.Model):
    channel = models.CharField(verbose_name="channel name", max_length=30)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.channel


"""Users may opt-in or opt-out for receiving notifications through a specific channel"""
class NotifChannelSetting(models.Model):
    notif_channel = models.OneToOneField(NotificationChannel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opt_out = models.BooleanField(verbose_name="opt this channel out", default=False)
    set_on = models.DateTimeField(default=timezone.now, editable=False)


"""A template is used for a general structure of notification messages for each channel"""
class NotificationTemplate(models.Model):
    notif_channel = models.OneToOneField(NotificationChannel, on_delete=models.CASCADE)
    template_name = models.CharField(verbose_name="notification template name", max_length=50)
    template_path = models.CharField(verbose_name="notification template path", max_length=250)


"""Notification triggers are initiators of the notification to be pushed out to the users. 
    There could be different triggers, such as new listing in near areas, someone rented or 
    buying one’s saved listing, etc"""
class NotificationTrigger(models.Model):
    name = models.CharField(verbose_name="trigger name", max_length=50, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    user_can_opt_out = models.BooleanField(default=True)

    def __str__(self):
        return self.name

"""Users can opt-in and opt-out notification triggers so that they decide to receive 
    a notification when the trigger is fired"""
class NotifTriggerSetting(models.Model):
    trigger = models.OneToOneField(NotificationTrigger, on_delete=models.CASCADE, verbose_name="notification trigger")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opt_out = models.BooleanField(default=False)
    setting_made_on = models.DateTimeField(default=timezone.now, editable=False)


"""Notification is sent to a target where a target may be a specific user, a group of users, a user group, or all"""
class NotifTargetType(models.Model):
    target_name = models.CharField(verbose_name="trigger name", max_length=50, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.target_name


"""Notification is an important part of a system. Notification can be sent to a specific user or group of users 
    triggered manually or automatically by the system"""
class Notification(models.Model):
    channel = models.ManyToManyField(NotificationChannel, verbose_name="notification channel to be used")
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="users to sent to", through="UserNotification")
    target_type = models.ForeignKey(NotifTargetType, on_delete=models.CASCADE, verbose_name="notification target type")
    notif_title = models.CharField(verbose_name="notification title", max_length=100, blank=False, null=False)
    notif_body = models.TextField(verbose_name="notification main message", blank=False, null=False)

    def __str__(self):
        return self.notif_title


"""Association class between Notification and User"""
class UserNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sent_on = models.DateTimeField(default=timezone.now, editable=False)
    read = models.BooleanField(default=False)