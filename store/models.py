from django.utils import timezone

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True
    )


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    country_of_origin = models.CharField(max_length=100)
    quality = models.CharField(max_length=100)
    check_healthiness = models.CharField(max_length=100)
    min_weight = models.DecimalField(max_digits=5, decimal_places=5)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

