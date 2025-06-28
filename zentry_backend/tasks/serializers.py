from rest_framework import serializers
from .models import Project, Task, TaskComment
from users.serializers import UserProfileSerializer

class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserProfileSerializer(read_only=True)
    members = UserProfileSerializer(many=True, read_only=True)
    member_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    task_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'emoji', 'created_by', 
            'members', 'member_ids', 'task_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by']

    def get_task_count(self, obj):
        return obj.tasks.count()

    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        project = Project.objects.create(**validated_data)
        if member_ids:
            project.members.set(member_ids)
        return project

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserProfileSerializer(read_only=True)
    created_by = UserProfileSerializer(read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority', 'emoji',
            'project', 'project_name', 'assigned_to', 'assigned_to_id', 
            'created_by', 'experience_reward', 'due_date', 'completed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'completed_at']

    def update(self, instance, validated_data):
        # Handle task completion
        if 'status' in validated_data and validated_data['status'] == 'completed' and instance.status != 'completed':
            instance.complete_task()
        return super().update(instance, validated_data)

class TaskCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = TaskComment
        fields = ['id', 'content', 'user', 'created_at']
        read_only_fields = ['user']

class TaskDetailSerializer(TaskSerializer):
    comments = TaskCommentSerializer(many=True, read_only=True)
    
    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['comments']
