from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PipelineRun, PipelineStep
from .serializers import PipelineRunSerializer, PipelineStepSerializer

class XRayViewSet(viewsets.ModelViewSet):
    """
    API to ingest Runs and Steps.
    """
    queryset = PipelineRun.objects.all()
    serializer_class = PipelineRunSerializer

    @action(detail=True, methods=['post'])
    def log_step(self, request, pk=None):
        """
        Custom endpoint to append a step to an existing Run.
        URL: /api/runs/{run_id}/log_step/
        """
        run = self.get_object()
        serializer = PipelineStepSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(run=run)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)