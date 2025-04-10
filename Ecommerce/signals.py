import os
import re
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils.html import strip_tags
from .models import Blog
from django.conf import settings


def extract_image_paths(content):
    """Extrait les chemins d'image dans le champ CKEditor."""
    return re.findall(r'src="([^"]+)"', content)


@receiver(pre_save, sender=Blog)
def delete_unused_images_on_update(sender, instance, **kwargs):
    try:
        if not instance.pk:
            return

        old_instance = Blog.objects.get(pk=instance.pk)
        old_images = set(extract_image_paths(old_instance.contenu))
        new_images = set(extract_image_paths(instance.contenu))

        unused_images = old_images - new_images

        for img_path in unused_images:
            if img_path.startswith(settings.MEDIA_URL):
                relative_path = img_path.replace(settings.MEDIA_URL, "")
                file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
                if os.path.exists(file_path):
                    os.remove(file_path)
    except Blog.DoesNotExist:
        pass


@receiver(post_delete, sender=Blog)
def delete_all_images_on_delete(sender, instance, **kwargs):
    """Supprime toutes les images d’un article supprimé."""
    for img_path in extract_image_paths(instance.contenu):
        if img_path.startswith(settings.MEDIA_URL):
            relative_path = img_path.replace(settings.MEDIA_URL, "")
            file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            if os.path.exists(file_path):
                os.remove(file_path)
