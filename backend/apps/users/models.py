from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model for the digital signage system.
    """
    ROLE_CHOICES = [
        ('admin', _('Administrator')),
        ('manager', _('Manager')),
        ('technician', _('Technician')),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='technician',
        verbose_name=_('Role')
    )

    agency = models.ForeignKey(
        'agencies.Agency',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name=_('Agency')
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Phone')
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
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        if not full_name:
            return self.username
        return full_name
