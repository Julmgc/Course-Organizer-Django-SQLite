from accounts.permissions import Facilitator, Instructor
from rest_framework import  status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Submissions
from .serializers import SubmissionSerializer
from activities.models import Activities



class ActivitySubmissionView(APIView):
    authentications_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, activity_id=''):
      activity = Activities.objects.get(id=activity_id)
      if not activity:
          return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
      data = request.data
      user = request.user
      if user.is_staff or user.is_superuser:
          return Response({"errors": "Only students can submit an activity."}, status=status.HTTP_403_FORBIDDEN)
      
      submission = Submissions.objects.create(grade=None, repo=data["repo"], user_id=user.id, activity_id=activity_id)
      serializer = SubmissionSerializer(submission)
      
      return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubmissionView(APIView):
    authentications_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.is_staff or user.is_superuser:
            submissions = Submissions.objects.all()
            serializer = SubmissionSerializer(submissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        submissions = Submissions.objects.get(user=user.id)
        serializer = SubmissionSerializer(submissions)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmissionGradeView(APIView):
    authentications_classes = [TokenAuthentication]
    permission_classes = [Instructor, Facilitator]

    def put(self, request, submission_id=''):


        submission = Submissions.objects.get(id=submission_id)
        if not submission:
            return Response({"errors": "invalid submission_id"}, status=status.HTTP_404_NOT_FOUND)
        grade = request.data["grade"]
        submission.grade = grade
        submission.save()
        serializer = SubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_200_OK)


