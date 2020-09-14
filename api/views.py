from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from .models import Tasker


class HomeView(ModelViewSet):
    queryset = Tasker.objects.all().order_by('state')
    serializer_class = TaskSerializer
