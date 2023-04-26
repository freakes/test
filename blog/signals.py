from .models import *
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, post_migrate, m2m_changed
from .models import Temporary
from django.core import serializers


@receiver([post_save, post_migrate], sender=Post)
@receiver([post_save, post_migrate], sender=Comment)
@receiver([post_save, post_migrate], sender=Tag)
@receiver([post_save, post_migrate], sender=Like)
def save_changes(sender, instance, **kwargs):
    current_state = Temporary(
        JsonData=serializers.serialize('json', [instance, ]),
        action='create'
    )
    current_state.save()

    Temporary.objects.filter(EndDate__isnull=True).update(
        EndDate=timezone.now()
    )


@receiver(m2m_changed, sender=Post.tags.through)
def save_post_changes(sender, instance, **kwargs):
    current_state = Temporary(
        JsonData=serializers.serialize('json', [instance, ]),
        action='edit'
    )
    current_state.save()

    Temporary.objects.filter(EndDate__isnull=True).update(
        EndDate=timezone.now()
    )


@receiver([post_delete], sender=Post)
@receiver([post_delete], sender=Comment)
@receiver([post_delete], sender=Tag)
@receiver([post_delete], sender=Like)
def save_changes(sender, instance, **kwargs):
    current_state = Temporary(
        JsonData=serializers.serialize('json', [instance, ]),
        action='delete'
    )
    current_state.save()

    Temporary.objects.filter(EndDate__isnull=True).update(
        EndDate=timezone.now()
    )
