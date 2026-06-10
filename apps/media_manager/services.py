from django.contrib.contenttypes.models import ContentType

from apps.media_manager.models import Media


class MediaService:

    @staticmethod
    def upload_single(
        *,
        instance,
        file,
        category,
        media_type=Media.MediaType.IMAGE,
    ):
        """
        Upload single media.
        """

        if not file:
            return None

        content_type = ContentType.objects.get_for_model(
            instance
        )

        media = Media.objects.create(
            content_type=content_type,
            object_id=instance.id,
            media_type=media_type,
            category=category,
            file=file,
            original_name=file.name,
            file_size=file.size,
            mime_type=getattr(
                file,
                "content_type",
                ""
            ),
        )

        return media

    @staticmethod
    def replace_single(
        *,
        instance,
        file,
        category,
        media_type=Media.MediaType.IMAGE,
    ):
        """
        Delete old and create new.
        """

        MediaService.delete_single_by_category(
            instance=instance,
            category=category,
        )

        return MediaService.upload_single(
            instance=instance,
            file=file,
            category=category,
            media_type=media_type,
        )

    @staticmethod
    def upload_multiple(
        *,
        instance,
        files,
        category,
        media_type=Media.MediaType.IMAGE,
    ):
        """
        Upload multiple files.
        """

        content_type = ContentType.objects.get_for_model(
            instance
        )

        media_objects = []

        for order, file in enumerate(
            files,
            start=1
        ):
            media = Media.objects.create(
                content_type=content_type,
                object_id=instance.id,
                media_type=media_type,
                category=category,
                file=file,
                original_name=file.name,
                file_size=file.size,
                mime_type=getattr(
                    file,
                    "content_type",
                    ""
                ),
                display_order=order,
            )

            media_objects.append(media)

        return media_objects

    @staticmethod
    def delete_media(
        media,
    ):
        """
        Delete media file + db record.
        """

        if media.file:
            media.file.delete(
                save=False
            )

        media.delete()

    @staticmethod
    def delete_single_by_category(
        *,
        instance,
        category,
    ):
        """
        Used for avatar replacement.
        """

        content_type = ContentType.objects.get_for_model(
            instance
        )

        media_items = Media.objects.filter(
            content_type=content_type,
            object_id=instance.id,
            category=category,
        )

        for media in media_items:
            MediaService.delete_media(
                media
            )