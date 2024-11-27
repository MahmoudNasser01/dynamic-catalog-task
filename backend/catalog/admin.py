from django.contrib import admin
from .models import Category, AttributeDefinition, Product, AttributeValue

# Inline model for AttributeDefinition
class AttributeDefinitionInline(admin.TabularInline):
    model = AttributeDefinition
    extra = 1  # Number of empty forms to display


# Admin for Category with AttributeDefinition inline
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [AttributeDefinitionInline]


# Inline model for AttributeValue
class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1  # Number of empty forms to display


# Admin for Product with AttributeValue inline
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'description')
    list_filter = ('category',)
    inlines = [AttributeValueInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'images', 'category')
        }),
    )


# Admin for AttributeDefinition (optional, in case you need a standalone management interface)
@admin.register(AttributeDefinition)
class AttributeDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'data_type', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


# Admin for AttributeValue (optional, in case you need a standalone management interface)
@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    search_fields = ('product__name', 'attribute__name', 'value')
    list_filter = ('attribute__category',)
