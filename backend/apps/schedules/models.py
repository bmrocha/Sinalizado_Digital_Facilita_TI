from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Schedule(models.Model):
    """
    Model for content scheduling.
    """
    DAYS_OF_WEEK = [
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    ]

    content = models.ForeignKey(
        'content.Content',
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name=_('Content')
    )

    start_time = models.TimeField(
        verbose_name=_('Start Time')
    )

    end_time = models.TimeField(
        verbose_name=_('End Time')
    )

    days_of_week = models.JSONField(
        default=list,
        help_text=_('List of days (0=Monday, 6=Sunday)'),
        verbose_name=_('Days of Week')
    )

    priority = models.PositiveIntegerField(
        default=1,
        help_text=_('Higher number = higher priority'),
        verbose_name=_('Priority')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )

    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')
        ordering = ['-priority', 'start_time']

    def __str__(self):
        return f"{self.content.title} - {self.start_time} to {self.end_time}"

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(_('End time must be after start time.'))

        # Check for overlapping schedules for the same content on same days
        overlapping = Schedule.objects.filter(
            content=self.content,
            is_active=True
        ).exclude(pk=self.pk).filter(
            models.Q(start_time__lt=self.end_time, end_time__gt=self.start_time)
        )

        for schedule in overlapping:
            if set(self.days_of_week) & set(schedule.days_of_week):
                raise ValidationError(_('Schedule overlaps with existing schedule.'))

    def get_days_display(self):
        """
        Return human-readable days of week.
        """
        return [dict(self.DAYS_OF_WEEK)[day] for day in self.days_of_week if day in dict(self.DAYS_OF_WEEK)]
