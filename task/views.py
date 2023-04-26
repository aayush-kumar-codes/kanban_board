from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import BoardSerializer, TaskSerializer
from .models import Board, Task


class BoardView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        boards = Board.objects.filter(user=request.user.id)
        serailzer = BoardSerializer(boards, many=True)
        return Response(data={
            "error": False,
            "data": serailzer.data
        })

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = BoardSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                "error": True,
                "message": "'name' is the required field"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(data={
            "error": False,
            "data": serializer.data
        })

    def patch(self, request, id):
        try:
            board = Board.objects.get(id=id)
        except Board.DoesNotExist:
            return Response(data={
                "error": True,
                "message": "Invalid Board Id"
            })

        if request.user.id != board.user_id:
            return Response(data={
                "error": True,
                "message": "Invalid User"
            })

        request.data['user'] = request.user.id

        serializer = BoardSerializer(instance=board, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data={
                "error": True,
                "message": "'name' is the required field"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(data={
            "error": False,
            "data": serializer.data
        })

    def delete(self, request, id):
        try:
            board = Board.objects.get(id=id)
        except Board.DoesNotExist:
            return Response(data={
                "error": True,
                "message": "Invalid Board Id"
            })

        if request.user.id != board.user_id:
            return Response(data={
                "error": True,
                "message": "Invalid User"
            })

        board.delete()

        return Response(data={
            "error": False,
            "message": "Board deleted successfully!"
        })


class TaskView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        tasks = Board.objects.filter(user=request.user.id)
        serailzer = BoardSerializer(tasks, many=True)
        return Response(data={
            "error": False,
            "data": serailzer.data
        })

    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                "error": True,
                "message": f"'task_description' and 'board' are required fields"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(data={
            "error": False,
            "data": serializer.data
        })

    def patch(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response(data={
                "error": True,
                "message": "Invalid Task Id"
            })

        if request.user.id != task.board.user_id:
            return Response(data={
                "error": True,
                "message": "Invalid User"
            })

        serializer = TaskSerializer(instance=task, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data={
                "error": True,
                "message": f"{serializer.errors.keys()} is the required field"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(data={
            "error": False,
            "data": serializer.data
        })

    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response(data={
                "error": True,
                "message": "Invalid Task Id"
            })

        if request.user.id != task.board.user_id:
            return Response(data={
                "error": True,
                "message": "Invalid User"
            })

        task.delete()
 
        return Response(data={
            "error": False,
            "message": "Task deleted successfully!"
        })
