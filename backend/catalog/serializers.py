from rest_framework import serializers
from .models import Product, Category, AttributeDefinition, AttributeValue


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeDefinition
        fields = ['id', 'name', 'data_type']


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.SerializerMethodField()
    class Meta:
        model = AttributeValue
        fields = ['attribute_name', 'value']


    def get_attribute_name(self, instance):
        return instance.attribute.name


class ProductSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'images', 'category', 'attributes']


    def get_attributes(self, instance):
        return AttributeValueSerializer(instance.attribute_values.all(), many=True).data