from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from apps.products.models import ProductImage


class Command(BaseCommand):
    help = 'Upload local media images to Cloudinary'

    def handle(self, *args, **kwargs):
        images = ProductImage.objects.all()
        if not images.exists():
            self.stdout.write(self.style.WARNING('No product images found in database.'))
            return

        media_root = Path(settings.MEDIA_ROOT)
        uploaded = 0
        skipped = 0
        missing = 0

        for img_obj in images:
            if not img_obj.image:
                continue

            name = img_obj.image.name

            # Already a Cloudinary URL — skip
            if name.startswith('http'):
                skipped += 1
                continue

            local_path = media_root / name
            if not local_path.exists():
                self.stdout.write(f'  MISSING: {name}')
                missing += 1
                continue

            with open(local_path, 'rb') as f:
                img_obj.image.save(name, File(f), save=True)
                uploaded += 1
                self.stdout.write(f'  UPLOADED: {name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. Uploaded: {uploaded}, Already OK: {skipped}, Missing: {missing}'
        ))
