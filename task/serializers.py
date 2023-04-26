from rest_framework import serializers

from .models import Board, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'user', 'name', 'added_on', 'updated_on', 'tasks']

    def get_tasks(self, obj):
        board_tasks = obj.board_tasks.all()
        if not board_tasks:
            return []
        return TaskSerializer(board_tasks, many=True).data
