from django.db import models
from django.utils.translation import gettext_lazy as _


class Content(models.Model):
    """
    Model for digital content (images, videos, links).
    """
    TYPE_CHOICES = [
        ('link', _('Link')),
        ('image', _('Image')),
        ('video', _('Video')),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name=_('Title')
    )

    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )

    content_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name=_('Content Type')
    )

    url = models.URLField(
        blank=True,
        verbose_name=_('URL')
    )

    file = models.FileField(
        upload_to='content/',
        blank=True,
        null=True,
        verbose_name=_('File')
    )

    duration = models.PositiveIntegerField(
        default=30,
        help_text=_('Duration in seconds'),
        verbose_name=_('Duration')
    )

    agency = models.ForeignKey(
        'agencies.Agency',
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name=_('Agency')
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
        verbose_name = _('Content')
        verbose_name_plural = _('Contents')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.content_type == 'link' and not self.url:
            raise ValidationError(_('URL is required for link content.'))
        if self.content_type in ['image', 'video'] and not self.file:
            raise ValidationError(_('File is required for image/video content.'))

    def get_content_url(self):
        """
        Return the appropriate URL for the content.
        """
        if self.content_type == 'link':
            return self.url
        elif self.file:
            return self.file.url
        return None
