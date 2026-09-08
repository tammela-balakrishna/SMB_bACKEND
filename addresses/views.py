from django.db import transaction

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomerAddress
from .serializers import CustomerAddressSerializer


class CustomerAddressViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerAddress.objects.filter(
            customer=self.request.user,
        )

    def perform_create(self, serializer):
        customer = self.request.user
        is_default = serializer.validated_data.get(
            "is_default",
            False,
        )

        with transaction.atomic():
            if is_default:
                CustomerAddress.objects.filter(
                    customer=customer,
                    is_default=True,
                ).update(
                    is_default=False,
                )

            has_default = CustomerAddress.objects.filter(
                customer=customer,
                is_default=True,
            ).exists()

            serializer.save(
                customer=customer,
                is_default=is_default or not has_default,
            )

    def perform_update(self, serializer):
        customer = self.request.user
        is_default = serializer.validated_data.get(
            "is_default",
            serializer.instance.is_default,
        )

        with transaction.atomic():
            if is_default:
                CustomerAddress.objects.filter(
                    customer=customer,
                    is_default=True,
                ).exclude(
                    pk=serializer.instance.pk,
                ).update(
                    is_default=False,
                )

            serializer.save(
                customer=customer,
                is_default=is_default,
            )

    def perform_destroy(self, instance):
        customer = self.request.user
        was_default = instance.is_default

        with transaction.atomic():
            instance.delete()

            if was_default:
                next_address = (
                    CustomerAddress.objects.filter(
                        customer=customer,
                    )
                    .order_by("-created_at")
                    .first()
                )

                if next_address:
                    next_address.is_default = True
                    next_address.save(
                        update_fields=[
                            "is_default",
                            "updated_at",
                        ],
                    )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="set-default",
    )
    def set_default(self, request, pk=None):
        address = self.get_object()

        with transaction.atomic():
            CustomerAddress.objects.filter(
                customer=request.user,
                is_default=True,
            ).exclude(
                pk=address.pk,
            ).update(
                is_default=False,
            )

            address.is_default = True
            address.save(
                update_fields=[
                    "is_default",
                    "updated_at",
                ],
            )

        return Response(
            CustomerAddressSerializer(
                address,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )