# core/admin.py
from django.contrib import admin
from .models import PipelineRun, PipelineStep

class PipelineStepInline(admin.TabularInline):
    model = PipelineStep
    extra = 0
    readonly_fields = ('step_name', 'step_type', 'inputs', 'outputs', 'metadata', 'created_at')
    can_delete = False

@admin.register(PipelineRun)
class PipelineRunAdmin(admin.ModelAdmin):
    list_display = ('pipeline_name', 'id', 'start_time')
    inlines = [PipelineStepInline]