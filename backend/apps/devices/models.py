from django.db import models
from django.utils.translation import gettext_lazy as _


class Device(models.Model):
    """
    Model for Raspberry Pi devices.
    """
    ORIENTATION_CHOICES = [
        ('horizontal', _('Horizontal')),
        ('vertical', _('Vertical')),
    ]

    STATUS_CHOICES = [
        ('online', _('Online')),
        ('offline', _('Offline')),
        ('maintenance', _('Maintenance')),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name=_('Device Name')
    )

    agency = models.ForeignKey(
        'agencies.Agency',
        on_delete=models.CASCADE,
        related_name='devices',
        verbose_name=_('Agency')
    )

    ip_address = models.GenericIPAddressField(
        protocol='IPv4',
        verbose_name=_('IP Address')
    )

    mac_address = models.CharField(
        max_length=17,
        blank=True,
        help_text=_('Format: XX:XX:XX:XX:XX:XX'),
        verbose_name=_('MAC Address')
    )

    orientation = models.CharField(
        max_length=20,
        choices=ORIENTATION_CHOICES,
        default='horizontal',
        verbose_name=_('Screen Orientation')
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='offline',
        verbose_name=_('Status')
    )

    last_seen = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Last Seen')
    )

    version = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Software Version')
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
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')
        ordering = ['agency', 'name']
        unique_together = ['agency', 'ip_address']

    def __str__(self):
        return f"{self.name} ({self.ip_address}) - {self.agency.name}"

    def update_status(self, status, version=None):
        """
        Update device status and last seen time.
        """
        from django.utils import timezone
        self.status = status
        self.last_seen = timezone.now()
        if version:
            self.version = version
        self.save(update_fields=['status', 'last_seen', 'version'])

    def get_current_content(self):
        """
        Get the content that should be displayed now based on schedules.
        """
        from django.utils import timezone
        from schedules.models import Schedule

        now = timezone.now()
        current_time = now.time()
        current_day = now.weekday()  # 0=Monday, 6=Sunday

        # Find active schedules for this agency's content that match current time and day
        schedules = Schedule.objects.filter(
            content__agency=self.agency,
            content__is_active=True,
            is_active=True,
            days_of_week__contains=[current_day],
            start_time__lte=current_time,
            end_time__gte=current_time
        ).select_related('content').order_by('-priority')

        if schedules.exists():
            return schedules.first().content

        return None
