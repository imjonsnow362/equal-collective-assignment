# core/models.py
import uuid
from django.db import models

class PipelineRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pipeline_name = models.CharField(max_length=255, help_text="e.g. competitor-selection")
    start_time = models.DateTimeField(auto_now_add=True)
    tags = models.JSONField(default=dict, blank=True, help_text="Metadata like version, region")

    def __str__(self):
        return f"{self.pipeline_name} - {self.id}"

class PipelineStep(models.Model):
    STEP_TYPES = [
        ('LLM', 'LLM Call'),
        ('FILTER', 'Filtering Logic'),
        ('API', 'External API'),
        ('RANK', 'Ranking Algo'),
        ('DECISION', 'Final Decision'),
    ]

    run = models.ForeignKey(PipelineRun, on_delete=models.CASCADE, related_name='steps')
    step_name = models.CharField(max_length=255)
    step_type = models.CharField(max_length=20, choices=STEP_TYPES, default='FILTER')
    
    # The Core "X-Ray" Data
    inputs = models.JSONField(default=dict, blank=True)
    outputs = models.JSONField(default=dict, blank=True)
    
    # Metadata for debugging (e.g., "reasoning": "Removed because price > $50")
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']