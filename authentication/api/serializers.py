from authentication.models import User
from rest_framework import serializers
from role.models import Role



class  UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'created_at', 'updated_at']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only
    user_type_id = serializers.IntegerField()  # Change to accept user_type_id as an integer

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'user_type_id') 

    def create(self, validated_data):
        # Fetch the Role instance based on the provided user_type_id
        try:
            role = Role.objects.get(id=validated_data['user_type_id'])  # Use ID to get Role
        except Role.DoesNotExist:
            raise serializers.ValidationError({"user_type_id": "Invalid user type."})

        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=role  # Assign the Role instance to user_type
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user