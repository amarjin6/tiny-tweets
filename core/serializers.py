from rest_framework import serializers
import os

ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp', 'gif']


class ImageSerializer(serializers.ModelSerializer):
    def validate_extension(image):
        extension = os.path.splitext(image)[1].replace('.', '')
        if extension.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            raise serializers.ValidationError(
                {'status': f'Invalid uploaded image type: {image}'}
            )
