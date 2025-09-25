from django.urls import path


from role.api.views import EditRoleAPIView, RoleDetailView, RoleListCreateView




urlpatterns = [
    path('roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),
    path('edit-role/<int:pk>/', EditRoleAPIView.as_view(), name='EditRoleAPIView'),
    
]