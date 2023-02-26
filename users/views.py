from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from users import serializers, models as u_models


class MyHomeUserGroupListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        group_serializer = serializers.MyHomeUserGroupSerializer()




class MyHomeUserListCreateView(generics.ListCreateAPIView):
    """
    View to create a user and view list of users
    """
    serializer_class = serializers.MyHomeUserSerializer
    queryset = u_models.MyHomeUser.objects.all()
    permission_classes = [AllowAny]


    def get(self, request, format=None):
        """
        Get list of users except the current user
        """
        user_model = u_models.MyHomeUser
        users = user_model.objects.exclude(pk=request.user.pk).order_by('pk')
        user_serializer = self.get_serializer(users, many=True)

        return Response(user_serializer.data)

    def post(self, request, format=None):
        """
        Save user and set password
        """
        user_data = request.data
        password = user_data.get('password')
        email = user_data.get('email')
        
        user_model = u_models.MyHomeUser
        if user_model.objects.filter(email=email).exists():
            return Response(data="User with this email already registered, please signin or use different email!", 
                            status=status.HTTP_404_NOT_FOUND)

        user_serializer = self.get_serializer(data=user_data)
        # print("USER: ",user_serializer)
        if user_serializer.is_valid():
            saved_instance = user_serializer.save()
            saved_instance.set_password(password)
            saved_instance.save()
            return Response(user_serializer.data)
        else:
            return Response("Data error!")


    # def perform_create(self, serializer):
    #     group_id = self.request.data["user_group"]
    #     group_serializer = serializers.MyHomeUserGroupSerializer(pk=group_id)
    #     serializer.save(user_group=group_serializer)
    #     return super().perform_create(serializer)


class MyHomeUserDetailUpdateView(generics.RetrieveUpdateAPIView):
    """
    View to update and view a user data
    """
    serializer_class = serializers.MyHomeUserSerializer
    queryset = u_models.MyHomeUser.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, pk=None, format=None):
        """
        Handler method to get a specific user detail
        """
        # user_model = u_models.MyHomeUser
        # user_instance= user_model.objects.filter(pk=pk)
        # # print("USER: ", user_instance)
        # user_serializer = self.get_serializer(user_instance)
        user =  request.user
        print("=================>: ",user)
        if user.is_authenticated:
            return Response(data=serializers.MyHomeUserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response(data="User is not authenticated!", status=status.HTTP_401_UNAUTHORIZED)

    

    def put(self, request, pk=None, format=None):
        """
        Handler method to update user and set user group
        """
        user_group_id = request.data['user_group']
        user_group_model = u_models.MyHomeUserGroup

        if user_group_model.objects.filter(pk=user_group_id).exists():
            user_group_obj = user_group_model.objects.get(pk=user_group_id)
        else: 
            return Response("User group does not exist!")

        user_instance = u_models.MyHomeUser.objects.get(pk=pk)
        user_serializer = self.get_serializer(user_instance, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save(user_group=user_group_obj)
            return Response(user_serializer.data)

        return Response("Error")