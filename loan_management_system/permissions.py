from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.profile.is_super_admin == True

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.profile.is_super_admin == True


class IsSuperAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.profile.is_super_admin == True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user.profile.is_super_admin == True


class IsStaffOrAdmin(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        return user.profile.user_type in ['admin', 'staff']

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.profile.user_type in ['admin', 'staff']


class IsStaffOrAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.profile.user_type in ['admin', 'staff']

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user.profile.user_type in ['admin', 'staff']


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        print(obj)
        return True


class IsOwnerOrStaffOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.method in ['GET', 'PUT', 'PATCH']

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user) or (request.user.profile.user_type in ['staff', 'admin'])
