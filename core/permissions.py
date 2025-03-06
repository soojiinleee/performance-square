from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    message = "이 리뷰를 수정할 권한이 없습니다. 작성자만 수정 할 수 있습니다."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
