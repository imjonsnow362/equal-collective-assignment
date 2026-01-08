from rest_framework import serializers
from .models import PipelineRun, PipelineStep

class PipelineStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = PipelineStep
        fields = '__all__'
        read_only_fields = ['run']  # We link it manually in the view

class PipelineRunSerializer(serializers.ModelSerializer):
    steps = PipelineStepSerializer(many=True, read_only=True)

    class Meta:
        model = PipelineRun
        fields = '__all__'