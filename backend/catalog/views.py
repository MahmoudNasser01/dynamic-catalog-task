from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category, AttributeDefinition
from .serializers import ProductSerializer, CategorySerializer, AttributeSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product, AttributeValue
from .serializers import ProductSerializer
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer






class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category__name', 'price']
    search_fields = ['name', 'description']

    @swagger_auto_schema(
        operation_description="Search for products based on name and/or dynamic attributes.",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search term for product name or description",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'attributes',
                openapi.IN_QUERY,
                description=(
                    "Comma-separated attributes to filter by "
                    "(e.g., Model='Apple',Battery='1000'). Use quotes for exact matches."
                ),
                type=openapi.TYPE_STRING
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        search_query = request.query_params.get('search', None)
        attributes_query = request.query_params.get('attributes', None)

        # Validate that at least one query parameter is provided
        if not search_query and not attributes_query:
            return Response({"error": "At least one of 'search' or 'attributes' is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize querysets
        queryset = self.queryset
        filters = Q()
        filters_list = []

        # Handle search query
        if search_query:
            search_query = search_query.strip()
            filters |= Q(name__icontains=search_query) | Q(description__icontains=search_query)

        # Handle dynamic attributes filtering
        if attributes_query:
            try:
                attributes_query = attributes_query.strip()
                attribute_filters = attributes_query.split(",")
                # Initialize list to hold Q objects for each attribute filter
                attribute_qs = []
                for attribute_filter in attribute_filters:
                    if "=" in attribute_filter:
                        key, value = attribute_filter.split("=")
                        key = key.strip()
                        value = value.strip().strip('"')  # Remove quotes for exact match
                        print(f"Filtering by attribute: {key} = {value}")
                        attribute_qs.append(
                            Q(attribute_values__attribute__name=key, attribute_values__value=value)
                        )
                        print(Product.objects.filter(Q(attribute_values__attribute__name=key, attribute_values__value=value)).distinct())

                    else:
                        return Response({"error": f"Invalid attribute filter format: {attribute_filter}"}, status=status.HTTP_400_BAD_REQUEST)

                # Combine the Q objects with AND logic
                filters_list = attribute_qs

            except Exception as e:
                return Response({"error": f"Invalid attributes format: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Apply filters and prefetch related attribute values to avoid duplicate results
        for filter in filters_list:
            queryset = queryset.filter(filter).prefetch_related('attribute_values').distinct()


        # Check if the queryset returns any results
        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        # Serialize and return the response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class CategoryAttributesView(APIView):

    def get(self, request, category_id):
        try:
            # Fetch the category by ID
            category = Category.objects.get(id=category_id)

            # Get all attributes related to this category
            attributes = AttributeDefinition.objects.filter(category=category)

            # Serialize the attributes
            serializer = AttributeSerializer(attributes, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)