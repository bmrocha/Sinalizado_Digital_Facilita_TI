from rest_framework import serializers
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    content_title = serializers.CharField(source='content.title', read_only=True)
    agency_name = serializers.CharField(source='content.agency.name', read_only=True)
    days_display = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = [
            'id', 'content', 'content_title', 'agency_name',
            'start_time', 'end_time', 'days_of_week', 'days_display',
            'priority', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_days_display(self, obj):
        return obj.get_days_display()

    def validate(self, data):
        """
        Check for schedule conflicts.
        """
        content = data.get('content')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        days_of_week = data.get('days_of_week', [])
        instance = self.instance

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        # Check for overlapping schedules
        from django.db.models import Q
        overlapping = Schedule.objects.filter(
            content=content,
            is_active=True
        ).exclude(pk=instance.pk if instance else None).filter(
            Q(start_time__lt=end_time, end_time__gt=start_time)
        )

        for schedule in overlapping:
            if set(days_of_week) & set(schedule.days_of_week):
                raise serializers.ValidationError("Schedule overlaps with existing schedule.")

        return data
