from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from users import models as u_models


"""Custom Form for creating new user with all model required fields and repeated password"""
class MyHomeUserCreationForm(forms.ModelForm):
    
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Re-enter your password", widget=forms.PasswordInput)

    class Meta:
        model = u_models.MyHomeUser
        fields = ['email', 'first_name', 'last_name']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password doesn't match")
        
        return password2

    def save(self, commit=True):
        """Save hashed password"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

"""Custom Form for updating a user"""
class MyHomeUserUpdateForm(forms.ModelForm):
    
    password = ReadOnlyPasswordHashField()

    class Meta:
        model= u_models.MyHomeUser
        fields = ['email', 'first_name', 'last_name', 'password', 'user_group', 'is_active', 'is_blocked', 'is_admin']


"""Add forms to Custom user admin page"""
class MyHomeUserAdmin(BaseUserAdmin):

    #Forms to add and change MyHomeUser instances
    form = MyHomeUserUpdateForm
    add_form = MyHomeUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'user_group', 'is_admin', 'is_blocked')
    list_filter = ('is_admin',)
    fieldsets = ((None, {'fields': ('email', 'password',)}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'user_group', 'is_active', 'is_blocked')}),
                ('Permissions', {'fields': ('is_admin',"is_staff")}))

    add_fieldsets = (
                    (None, {'classes': ('wide',),
                             'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'), }),
                 )

    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()

"""Register the User model to the admin page"""
admin.site.register(u_models.MyHomeUser, MyHomeUserAdmin)

"""Unregister the default Group model from admin page"""
admin.site.unregister(Group)

#==============================================================================

"""Admin page custom User Group creating form"""
class MyHomeUserGroupCreationForm(forms.ModelForm):
    class Meta:
        model = u_models.MyHomeUserGroup
        fields = ['name', 'description']

"""Admin page custom User Group update form"""
class MyHomeUserGroupUpdateForm(forms.ModelForm):
    class Meta:
        model = u_models.MyHomeUserGroup
        fields = ['name', 'description']

"""Add the custom forms to the admin page"""
class MyHomeUserGroupAdmin(admin.ModelAdmin):
    form = MyHomeUserGroupUpdateForm
    add_form = MyHomeUserGroupCreationForm

    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']


"""Register the User Group to the admin page"""
admin.site.register(u_models.MyHomeUserGroup, MyHomeUserGroupAdmin)
admin.site.register(u_models.LoginHistory)
admin.site.register(u_models.Permission)
admin.site.register(u_models.Role)
admin.site.register(u_models.SystemAdminGroup)
admin.site.register(u_models.SystemAdmin)




