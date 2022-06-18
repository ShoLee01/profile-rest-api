from rest_framework import serializers

from profile_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing out APIView"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile objects."""

    class Meta:
        model = models.UserProfile
        fields =('id', 'email', 'name', 'password')
        extra_kwargs = { # Permite especificar algunas propiedades de los campos
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user."""
        user =models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password') # Elimina el password del diccionario
            instance.set_password(password) #Guarda la contraseña como hash

        return super().update(instance, validated_data) # para pasar los valores al 
        #método DRF update() existente, para manejar la actualización de los campos restantes.

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """A serializer for profile feed items."""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {
            'user_profile': {'read_only': True}
            }