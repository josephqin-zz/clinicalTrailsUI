from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    ElasticSearch = serializers.CharField(required=False, default=None, max_length=100)
    aas_on = serializers.BooleanField(required=False,default=False)
    Ontology = serializers.BooleanField(required=False, default=False)
    disease = serializers.CharField(required=False, default=None, max_length=100)
    age = serializers.CharField(required=False, default=None, max_length=100)
    gender = serializers.CharField(required=False, default=None, max_length=100)
    gene = serializers.CharField(required=False, default=None, max_length=100)
    aas = serializers.CharField(required=False, default=None, max_length=100)
    stage = serializers.CharField(required=False, default=None, max_length=100)
    grade = serializers.CharField(required=False, default=None, max_length=100)
    address = serializers.CharField(required=False, default=None, max_length=100)
    include_keywords = serializers.CharField(required=False, default=None, max_length=100)
    exclude_keywords = serializers.CharField(required=False, default=None, max_length=100)
