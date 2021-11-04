from accounts.permissions import Facilitator, Instructor
from rest_framework import  status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError
from .models import Activities
from .serializers import ActivitySerializer
from django.shortcuts import get_object_or_404

class ActivityView(APIView):
    authentications_classes = [TokenAuthentication]
    permission_classes = [Instructor, Facilitator]
    def post(self, request):
      try:
          data = request.data
          activity = Activities.objects.create(**data)
          serializer = ActivitySerializer(activity)
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      except IntegrityError:
          return Response({'error': 'Activity with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
      activities = Activities.objects.all()
      serializer = ActivitySerializer(activities, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

class ActivityViewQuery(APIView):
    authentications_classes = [TokenAuthentication]
    permission_classes = [Instructor, Facilitator]

    def put(self, request, activity_id=''):
        data = request.data
        activity = get_object_or_404(Activities, id=activity_id)

        if hasattr(activity, "submissions"):
            if activity.submissions.first():
              return Response({'error': 'You can not change an Activity with submissions'}, status=status.HTTP_400_BAD_REQUEST)
        title = data["title"]
        points = data["points"]
        activity.title = title
        activity.points = points
        activity.save()
        serializer = ActivitySerializer(activity)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    