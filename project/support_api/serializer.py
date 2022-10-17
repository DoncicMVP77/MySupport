from django.utils.text import slugify
from rest_framework import serializers

from .models import Message, Ticket


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    slug = serializers.SlugField(required=False, read_only=True)
    timestamp = serializers.ReadOnlyField()
    last_activity = serializers.ReadOnlyField()
    messages = serializers.SerializerMethodField(read_only=True)

    def get_messages(self, obj):
        qs = Message.objects.filter(ticket=obj)
        try:
            serializer = MessageSerializer(qs, many=True)
            return serializer.data
        except Exception as e:
            print(e)

    def update(self, instance, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data.get("title"))
        return super(TicketSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data.get("title"))
        return super(TicketSerializer, self).create(validated_data)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "slug",
            "user",
            "category",
            "title",
            "description",
            "status",
            "messages",
            "timestamp",
            "last_activity",
        ]


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    timestamp = serializers.ReadOnlyField()

    class Meta:
        model = Message
        fields = [
            'user',
            "ticket",
            'text',
            'timestamp',
        ]
