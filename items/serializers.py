from rest_framework import serializers
from .models import ItemCategory, Items, ItemImage
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['id', 'image', 'order']
        read_only_fields = ['id']


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'name']
        read_only_fields = ['id']

class ItemSerializers(serializers.ModelSerializer):
    images = ItemImageSerializer(many=True, required=False, read_only=True)
    category_name = serializers.CharField(source= 'category.name', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    posted_date = serializers.DateTimeField(read_only=True, format='%d %b %Y')
    uploaded_images = serializers.ListField(
        child= serializers.ImageField(max_length=None, use_url=True),
        write_only=True,
        required=False
    )

    class Meta:
        model = Items
        fields = '__all__'
        read_only_fields = [
            'id', 'first_name', 'last_name', 'category_name', 'title', 'discription',
            'posted_date', 'listing_type', 'price', 'location', 'status', 'images', 'uploaded_images'
        ]

        read_only_fields = ['id', 'first_name', 'last_name', 'posted_date']

    
    def validate_uploaded_images(self, upload_images):
        if upload_images and len(upload_images) > 3:
            raise serializers.ValidationError("Maximum 3 images allowed.")

        return upload_images


    def validate(self, validate_data):
        user_data = validate_data.pop('user')

        price = validate_data['price']
        listing_type = validate_data['listing_type']
        category = validate_data['category']


        if listing_type == 'buy' and (price is None or price <= 0):
            raise serializers.ValidationError("Price must me included or list it as free.")
        
        if not category:
            raise serializers.ValidationError("Select the category for item to be listed.") 
        
    
    @transaction.atomic
    def create(self, validate_data):
        uploaded_images = validate_data.pop('uploaded_images', [])

        if not uploaded_images:
            raise serializers.ValidationError({"uploaded_images": "At least one image is required."})

        item = Items.objects.create(**validate_data)

        for i, image_data in enumerate(uploaded_images):
            ItemImage.objects.create(
                item = item,
                image = image_data,
                order = i
            )
        
        return item