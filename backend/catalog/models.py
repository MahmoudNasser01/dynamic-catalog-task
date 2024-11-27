from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class AttributeDefinition(models.Model):
    name = models.CharField(max_length=255)
    data_type = models.CharField(
        max_length=50,
        choices=[
            ('string', 'String'),
            ('integer', 'Integer'),
            ('boolean', 'Boolean'),
            ('float', 'Float'),
        ]
    )
    category = models.ForeignKey(Category, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.data_type})"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.JSONField(default=list)  # Store image URLs as a list
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    product = models.ForeignKey(Product, related_name='attribute_values', on_delete=models.CASCADE)
    attribute = models.ForeignKey(AttributeDefinition, related_name='attribute_values', on_delete=models.CASCADE)
    value = models.TextField()  # Store values as text to handle various data types

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"
