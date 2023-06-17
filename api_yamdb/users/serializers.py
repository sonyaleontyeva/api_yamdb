from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'bio', 'role')
        model = User
        read_only_fields = ('role', )
