from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import DeviceToken, Notification
from .serializers import (
    DeviceTokenSerializer,
    NotificationSerializer,
)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Notification.objects
            .filter(user=self.request.user)
            .select_related("order")
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="read",
    )
    def mark_as_read(self, request, *args, **kwargs):
        notification = self.get_object()

        if not notification.is_read:
            notification.is_read = True
            notification.save(
                update_fields=[
                    "is_read",
                    "updated_at",
                ]
            )

        return Response(
            NotificationSerializer(
                notification,
                context={"request": request},
            ).data
        )

    @action(
        detail=False,
        methods=["patch"],
        url_path="read-all",
    )
    def mark_all_as_read(self, request, *args, **kwargs):
        updated_count = (
            self.get_queryset()
            .filter(is_read=False)
            .update(is_read=True)
        )

        return Response(
            {
                "detail": "All notifications marked as read.",
                "updated_count": updated_count,
            },
            status=status.HTTP_200_OK,
        )


class DeviceTokenViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceTokenSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return DeviceToken.objects.filter(
            user=self.request.user
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        platform = serializer.validated_data.get(
            "platform",
            DeviceToken.Platform.ANDROID,
        )

        device_token, created = DeviceToken.objects.update_or_create(
            token=token,
            defaults={
                "user": request.user,
                "platform": platform,
                "is_active": True,
            },
        )

        response_serializer = self.get_serializer(
            device_token
        )

        return Response(
            response_serializer.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            ),
        )