import re
from django.db import models # Prporciona el modelo de base de datos
from django.contrib.auth.models import AbstractBaseUser 
#proporciona la implementación central de un modelo de usuario, incluidas las contraseñas 
# hash y los restablecimientos de contraseña tokenizados.
from django.contrib.auth.models import PermissionsMixin # Propociona permisos de usuario como "is_superuser"
from django.contrib.auth.models import BaseUserManager # Proporciona metodos para crear usuarios
# Create your models here.
from django.conf import settings

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None): # Crea, guarda y retorna un usuario
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True #Tiene todos los permisos sin especificar 
        user.is_staff = True #Tiene permisos de para acceder al panel de administracion
        user.save(using=self._db) # slef._db es para asignar a una base de datos predeterminada
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) # Indica si el usuario esta activo
    is_staff = models.BooleanField(default=False) # Para que el usuario pueda acceder al panel de administracion

    objects = UserProfileManager() # Para que el manager sea accesible desde el modelo

    USERNAME_FIELD = 'email' # Para que el campo de usuario sea el email
    REQUIRED_FIELDS= ['name'] # Para que el usuario sea obligatorio

    def get_full_name(self): # Para que el objeto sea representable como un string
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self): # Para que el objeto sea representable como un string
        """Retrieve short name of user"""
        return self.name
    
    def __str__(self): # Para que el objeto sea representable como un string
        """Return string representation of our user"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Para que el usuario sea una clave foranea
        on_delete=models.CASCADE # Para que el usuario sea eliminado junto con su perfil
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text