from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users import models as u_models


class MyHomeUserGroupSerializer(ModelSerializer):
    class Meta:
        model = u_models.MyHomeUserGroup
        fields = '__all__'


class MyHomeUserSerializer(ModelSerializer):
    user_group = serializers.PrimaryKeyRelatedField(read_only=True)
    has_agent = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = u_models.MyHomeUser
        fields = ('id',
                    'email', 
                    'password', 
                    'first_name', 
                    'last_name',
                    'user_group', 
                    'is_active', 
                    'is_blocked', 
                    'is_admin', 
                    'is_staff', 
                    'last_login', 
                    'date_joined',
                    'has_agent')
        extra_kwargs = {'password': {'write_only': True}}
        # depth = 1

    def create(self, validated_data):
        user_group_id = self.context.get('request').data['user_group']
        user_group_obj = u_models.MyHomeUserGroup.objects.get(pk=user_group_id)
        return u_models.MyHomeUser.objects.create(user_group=user_group_obj, **validated_data)

    def get_has_agent(self, obj):
        from agents.models import AgentAdmin
        agent_admin_obj = AgentAdmin.objects.filter(admin=obj.id)
        if agent_admin_obj.exists():
            return True
        else:
            return False

    
    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     # instance.password = validated_data.get('password', instance.password)
    #     # instance.first_name = validated_data.get('first_name', instance.first_name)
    #     # instance.last_name = validated_data.get('last_name', instance.last_name)
    #     # instance.is_active = validated_data.get('is_active', instance.is_active)
    #     # instance.is_blocked = validated_data.get('is_blocked', instance.is_blocked)
    #     # instance.is_staff = validated_data.get('is_staff', instance.is_staff)
    #     # instance.is_admin = validated_data.get('is_admin', instance.is_admin)
    #     user_group_id = self.context.get('request').data['user_group']
    #     user_group_obj = u_models.MyHomeUserGroup.objects.get(pk=user_group_id)
    #     instance.user_group = user_group_obj
    #     instance.save()
    #     return instance