# apps/media_manager/serializers.py

from rest_framework import serializers

from apps.media_manager.models import Media


class MediaSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()

    class Meta:
        model = Media

        fields = (
            "id",
            "url",
            "category",
            "media_type",
            "original_name",
            "mime_type",
            "file_size",
            "display_order",
            "created_at",
        )

        read_only_fields = fields

    def get_url(self, obj):
        request = self.context.get("request")

        if not obj.file:
            return None

        if request:
            return request.build_absolute_uri(
                obj.file.url
            )

        return obj.file.url