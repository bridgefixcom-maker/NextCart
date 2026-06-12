from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True, db_index=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.name

    def _generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        qs = Category.objects.exclude(pk=self.pk)
        while qs.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug or self.name != self.__original_name:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)
        self.__original_name = self.name

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )

    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True, db_index=True)
    sku = models.CharField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.name

    def _generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        qs = Product.objects.exclude(pk=self.pk)
        while qs.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        return slug

    def _generate_sku(self):
        cat = slugify(self.category.name)[:3].upper()
        prod = slugify(self.name)[:5].upper()
        base = f'{cat}-{prod}'
        sku = base
        counter = 1
        qs = Product.objects.exclude(pk=self.pk)
        while qs.filter(sku=sku).exists():
            sku = f'{base}-{counter}'
            counter += 1
        return sku

    def save(self, *args, **kwargs):
        if not self.slug or self.name != self.__original_name:
            self.slug = self._generate_unique_slug()
        if not self.sku:
            self.sku = self._generate_sku()
        super().save(*args, **kwargs)
        self.__original_name = self.name

    @property
    def in_stock(self):
        return self.is_available and self.stock_quantity > 0

    @property
    def effective_price(self):
        return self.sale_price if self.sale_price else self.price

    @property
    def discount_percentage(self):
        if self.sale_price and self.sale_price < self.price:
            return round((1 - self.sale_price / self.price) * 100, 1)
        return 0

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/%Y/%m/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_images'

    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product, is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} - {"Primary" if self.is_primary else "Secondary"}'

