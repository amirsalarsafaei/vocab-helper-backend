from rest_framework.permissions import BasePermission

class IsOTPVerified(BasePermission):
    """
    Custom permission to only allow access to users who have verified their OTP.
    """

    def has_permission(self, request, view):
        # Assuming you store OTP verification status in user profile or session
        return request.user.is_authenticated and request.user.is_verified()
        

    

class AsyncIsOTPVerified(BasePermission):
    """
    Custom permission to only allow access to users who have verified their OTP.
    """

    async def has_permission(self, request, view):
        # Assuming you store OTP verification status in user profile or session
        return request.user.is_authenticated and request.user.is_verified()
        

    
