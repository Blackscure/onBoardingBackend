from rest_framework import  permissions, views, status
from rest_framework.response import Response
from rest_framework.views import APIView
from role.api.serilizers import RoleSerializer
from role.models import Role



class RoleListCreateView(APIView):
    
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        
        # Wrap the serialized data in a 'data' array
        data_array = {'data': serializer.data}
        
        return Response(data_array)

# Create Role

    def post(self, request):
        try:
            role_name = request.data.get('role_name', None)

            # Check if a Role with the same role_name already exists
            existing_role = Role.objects.filter(role_name=role_name).first()
            if existing_role:
                raise ValueError(f"A role with the name '{role_name}' already exists.")

            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                role = serializer.save()  # Save and get the created role instance
                return Response(
                    {
                        "message": f"Role '{role_name}' created successfully.",
                        "data": serializer.data  # Serialized data of the created role
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                raise ValueError("Invalid data. Unable to create the role.")

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
# Get individual role
class RoleDetailView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            role = Role.objects.get(pk=pk)
            serializer = RoleSerializer(role)
            return Response({
                'status': True,
                'message': 'Role fetched successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Role not found',
            }, status=status.HTTP_404_NOT_FOUND)

    # del a role
        
    def delete(self, request, pk):
            try:
                role = self.get_object(pk)
                role.delete()
                return Response(
                    {"success": f"Role with ID {pk} deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT
                )

            except Role.DoesNotExist:
                return Response(
                    {"error": f"Role with ID {pk} not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            



class EditRoleAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            getrole = Role.objects.get(pk=pk)
            serializer = RoleSerializer(getrole, data=request.data)
            if not serializer.is_valid():
                return Response({"status": "error","data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
            serializer.save()
     
            return Response({
                'status': True,
                'message':'Update Has been successful.',
                'data': serializer.data
            })


        except Exception as e:
                return Response({
                'status':False,
                'message':'We were not able to update role.',
                "error": str(e)
            })
        