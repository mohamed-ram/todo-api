import datetime

import pytz
from django.utils.text import slugify
from rest_framework import serializers

# Task serializer.
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(allow_blank=True, read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
    
    def create(self, validated_data):
        slug = slugify(validated_data['title'])
        return Task.objects.create(**validated_data, slug=slug)

    def update(self, instance, validated_data):
        # customize slug before saving.
        slug = slugify(validated_data['title'])
    
        # unnecessary fields.
        # instance.id = validated_data.get('id', instance.id)
        # instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', slug)
        instance.description = validated_data.get('description', instance.description)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.updated = validated_data.get('updated', datetime.datetime.now())
        instance.save()
        return instance


PRIORITY = (
    ('Hard', 'Hard'),
    ('Medium', 'Medium'),
    ('Easy', 'Easy'),
)

class TaskCustomSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    slug = serializers.SlugField(allow_blank=True, max_length=100, read_only=True)
    description = serializers.CharField(required=True, style={'base_template': 'textarea.html'})
    priority = serializers.ChoiceField(choices=PRIORITY)
    completed = serializers.BooleanField(default=False)
    timestamp = serializers.DateTimeField(read_only=True, allow_null=True)
    updated = serializers.DateTimeField(read_only=True, allow_null=True)
    
    def create(self, validated_data):
        slug = slugify(validated_data['title'])
        return Task.objects.create(**validated_data, slug=slug)
    
    def update(self, instance, validated_data):
        # customize slug before saving.
        slug = slugify(validated_data['title'])
        
        # unnecessary fields..
        # instance.id = validated_data.get('id', instance.id)
        # instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        # instance.updated = validated_data.get('updated', instance.updated)
        
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', slug)
        instance.description = validated_data.get('description', instance.description)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance


