from django.db import models


class Category(models.Model):
    # Each category may have a parent category (it is a recursive relationship)
    # in previous week I returned children on json response which is incorrect. now I return a category and a parent
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    def __str__(self):
        if self.parent:
            return f'{self.name} (Parent: {self.parent.name})'
        else:
            return self.name

    def get_children(self):
        """ Return the children (subcategories) of this category """
        return self.subcategories.all()

    def get_product_count(self, accumulator=0):
        """ recursive function using accumulator which is actively used in functional programming like ocaml"""
        accumulator += self.products.count()
        for subcategory in self.get_children():
            accumulator = subcategory.get_product_count(accumulator)

        return accumulator

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='products')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
