# core/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PipelineRun, PipelineStep
from .serializers import PipelineRunSerializer, PipelineStepSerializer

class XRayViewSet(viewsets.ModelViewSet):
    queryset = PipelineRun.objects.all()
    serializer_class = PipelineRunSerializer

    # --- ADD THESE TWO LINES TO DISABLE AUTH CHECKS ---
    authentication_classes = [] 
    permission_classes = []
    # --------------------------------------------------

    @action(detail=True, methods=['post'])
    def log_step(self, request, pk=None):
        run = self.get_object()
        serializer = PipelineStepSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(run=run)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)