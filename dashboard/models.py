from django.db import models
from django.utils.translation import ugettext_lazy as _


class processExecutions(models.Model):

    _STATUS_CHOICES = (
        ('pending', 'pending'),
        ('running', 'running'),
        ('completed', 'completed'),
    )
    _CATEGORY_CHOICES = (
        ('root', 'root'),
        ('child', 'child'),
    )
    process_title = models.CharField(
        _('Process Title'),
        max_length=254, 
        help_text=_('Text Field, 254, Characters.')
        )

    node_id = models.CharField(
        _('Node ID'),
        max_length=254, 
           blank=True,
        null=True,
    )
    node_type = models.CharField(
        _('Node Type'),
        max_length=254, 
        choices=_CATEGORY_CHOICES, 
        default='root'
    )
    start_time = models.DateTimeField(
        _('Started At'),
        auto_now_add=True,
        blank=True,
        null=True,
    )
    completed_at = models.DateTimeField(
        _('Completed At'),
        blank=True,
        null=True,
    )
    status = models.CharField(
        _('Execution Status'),
        max_length=50,
        help_text=_("Text Choice Field, 50, Characters."),
        choices=_STATUS_CHOICES,
        default='pending'
    )
    
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True,
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        _('Updated At'),
        auto_now=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Execution')
        verbose_name_plural = _('Executions')

    def __str__(self):
        return self.process_title