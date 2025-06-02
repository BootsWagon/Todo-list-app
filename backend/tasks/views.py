from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Max
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        Override get_queryset to ensure proper ordering of tasks
        """
        return Task.objects.all().order_by('status', 'order', '-updated_at')

    def perform_create(self, serializer):
        """
        Set the order for new tasks to be last in their status group
        """
        status = serializer.validated_data.get('status', 'UPCOMING')
        max_order = Task.objects.filter(status=status).aggregate(Max('order'))['order__max'] or 0
        serializer.save(order=max_order + 1)

    def perform_update(self, serializer):
        """
        Handle task updates, including status changes and reordering
        """
        old_status = self.get_object().status
        new_status = serializer.validated_data.get('status', old_status)
        
        # If status changed, adjust order
        if old_status != new_status:
            max_order = Task.objects.filter(status=new_status).aggregate(Max('order'))['order__max'] or 0
            serializer.save(order=max_order + 1)
        else:
            serializer.save()

    def partial_update(self, request, *args, **kwargs):
        """
        Handle PATCH requests for drag-and-drop reordering
        """
        instance = self.get_object()
        new_status = request.data.get('status', instance.status)
        new_order = request.data.get('order')

        if new_order is not None:
            # Reorder tasks in the same status column
            if new_status == instance.status:
                tasks_to_update = Task.objects.filter(
                    status=new_status,
                    order__gte=new_order
                ).exclude(id=instance.id)
                
                for task in tasks_to_update:
                    task.order += 1
                    task.save()
            else:
                # Moving to a different status column
                max_order = Task.objects.filter(status=new_status).aggregate(Max('order'))['order__max'] or 0
                new_order = max_order + 1

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data) 