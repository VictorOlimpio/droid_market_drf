from rest_framework import permissions
import ipdb


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        ipdb.set_trace()
        return obj.owner == request.user

