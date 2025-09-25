from django.urls import path


from authentication.api.views import EditUserAPIView, GetTokenView, GetUserView, LoginApiView, RegisterAPIView, SignOutApiView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('get-token/', GetTokenView.as_view(), name='get_token'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('user/', GetUserView.as_view(), name='get_user'),
    path('edit-user/<int:pk>/', EditUserAPIView.as_view(), name='EditUsersView'),
    path('signout/', SignOutApiView.as_view(), name='signout')

]