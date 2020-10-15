from rest_framework import serializers

from library.models.users import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
      model = User
      fields = ['first_name', 'email', 'country']