from django.db import models
from django.utils.translation import gettext_lazy as _


class Agency(models.Model):
    """
    Model for Sicoob agencies.
    """
    ORIENTATION_CHOICES = [
        ('horizontal', _('Horizontal')),
        ('vertical', _('Vertical')),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Name')
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Code')
    )

    address = models.TextField(
        blank=True,
        verbose_name=_('Address')
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Phone')
    )

    email = models.EmailField(
        blank=True,
        verbose_name=_('Email')
    )

    orientation = models.CharField(
        max_length=20,
        choices=ORIENTATION_CHOICES,
        default='horizontal',
        verbose_name=_('Screen Orientation')
    )

    hibernation_start = models.TimeField(
        default='18:00',
        verbose_name=_('Hibernation Start Time')
    )

    hibernation_end = models.TimeField(
        default='08:00',
        verbose_name=_('Hibernation End Time')
    )

    logo = models.FileField(
        upload_to='logos/',
        blank=True,
        null=True,
        verbose_name=_('Logo')
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
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"
