from rest_framework import serializers
from users.models import User, UserProfile
from demands.serializers import DemandSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'phone', 'ddd']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)
    demands = DemandSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile', 'demands')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)

        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        if 'profile' in validated_data.keys() and (not instance.is_staff):
            profile = instance.profile
            profile_data = validated_data.pop('profile')
            profile.phone = profile_data.get('phone', profile.phone)
            profile.ddd = profile_data.get('ddd', profile.ddd)
            profile.save()

        return instance
