from dataclasses import fields
from rest_framework import serializers

from .models import UserMails

class UserMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMails
        fields = ('id', 'email', )

