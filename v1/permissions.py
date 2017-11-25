from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    Permission to only allow owners of a resource edit it.
    '''

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True                

        # Write permissions are only allowed to the owner of a resource.
        return obj.owner == request.user


