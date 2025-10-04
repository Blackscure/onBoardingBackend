from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Form, Field
from .serializers import FormSerializer, FieldSerializer


# ------------------- FORM CRUD -------------------
class FormListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        forms = Form.objects.filter(user=request.user).order_by('-created_at')
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Form, pk=pk, user=user)

    def get(self, request, pk):
        form = self.get_object(pk, request.user)
        serializer = FormSerializer(form)
        return Response(serializer.data)

    def put(self, request, pk):
        form = self.get_object(pk, request.user)
        serializer = FormSerializer(form, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        form = self.get_object(pk, request.user)
        serializer = FormSerializer(form, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        form = self.get_object(pk, request.user)
        form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ------------------- FIELD CRUD -------------------
class FieldListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        fields = Field.objects.filter(form__user=request.user)
        serializer = FieldSerializer(fields, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FieldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FieldDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Field, pk=pk, form__user=user)

    def get(self, request, pk):
        field = self.get_object(pk, request.user)
        serializer = FieldSerializer(field)
        return Response(serializer.data)

    def put(self, request, pk):
        field = self.get_object(pk, request.user)
        serializer = FieldSerializer(field, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        field = self.get_object(pk, request.user)
        serializer = FieldSerializer(field, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        field = self.get_object(pk, request.user)
        field.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
