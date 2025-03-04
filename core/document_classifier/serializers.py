from rest_framework import serializers

class DocumentClassifierSerializer(serializers.Serializer):
    file = serializers.FileField()
    

class BulkUploadSerializer(serializers.Serializer):
    bulk_file = serializers.FileField(required=True)


