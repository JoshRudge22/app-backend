from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
        owner = serializers.ReadOnlyField(source='owner.username')

class Meta:
    model = Profile
    fields = [
        'id', 'owner', 'first_name', 'age', 'profile_image', 'gender', 'phone_number', 'email', 'is_owner'
    ]

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

