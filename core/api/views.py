from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Application
from .serializers import ApplicationSerializer

class ApplicationListView(APIView):
    def get(self, request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

# Create a new application
class ApplicationCreateView(APIView):
    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Automatically associate with the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve applications for a specific user
class ApplicationByIdView(APIView):
    def get(self, request, app_id):
        if app_id:
            try:
                application = Application.objects.get(id=app_id)
                serializer = ApplicationSerializer(application)
                return Response(serializer.data)
            except Application.DoesNotExist:
                return Response({"Error": "Application Does Not Exist"},status=400)   
            
class ApplicationUpdateView(APIView):
    def put(self, request, app_id):
            try:
                application = Application.objects.get(id=app_id)
                serializer = ApplicationSerializer(application, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Application.DoesNotExist:
                 return Response({"Error": "Application Does Not Exist"},status=400)   

class ApplicationDeleteView(APIView):
    def delete(self, request, app_id):
        try:
            application = Application.objects.get(id=app_id)
            application.delete()
            return Response({"Success": "Application Deleted Successfully"},status=200)
        except Application.DoesNotExist:
            return Response({"Error": "Application Does Not Exist"},status=400)   