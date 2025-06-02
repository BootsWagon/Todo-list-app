from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'status_display',
            'priority', 'priority_display', 'order', 'completed',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_title(self, value):
        """
        Validate the title field
        """
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value.strip()

    def validate_status(self, value):
        """
        Validate the status field
        """
        valid_statuses = dict(Task.STATUS_CHOICES).keys()
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        return value

    def validate_priority(self, value):
        """
        Validate the priority field
        """
        valid_priorities = dict(Task.PRIORITY_CHOICES).keys()
        if value not in valid_priorities:
            raise serializers.ValidationError(f"Invalid priority. Must be one of: {', '.join(valid_priorities)}")
        return value

    def validate_order(self, value):
        """
        Validate the order field
        """
        if value is not None and value < 0:
            raise serializers.ValidationError("Order must be a non-negative integer")
        return value 