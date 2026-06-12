import os
import sys
from pathlib import Path
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django

django.setup()

from apps.products.models import ProductImage

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / 'media'

migrated = 0
missing = 0

for image_obj in ProductImage.objects.all():
    if not image_obj.image:
        continue
    image_path = MEDIA_ROOT / image_obj.image.name
    if not image_path.exists():
        missing += 1
        print(f'MISSING: {image_obj.image.name}')
        continue
    with open(image_path, 'rb') as f:
        image_obj.image.save(image_obj.image.name, File(f), save=True)
        migrated += 1
        print(f'MIGRATED: {image_obj.image.name}')

print(f'Finished. Migrated {migrated} images, missing {missing} files.')
