from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""

    def has_object_permission(self, request, view, obj): # obj es el objeto que se va a editar
        """Check if user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS: # Verifica si el método es uno de los métodos seguros (get, head, options)
            return True

        return obj.id == request.user.id # Verifica si el usuario que esta intentando editar su perfil es el mismo que esta en la solicitud 


class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self, request, view, obj):
        """Check if user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id