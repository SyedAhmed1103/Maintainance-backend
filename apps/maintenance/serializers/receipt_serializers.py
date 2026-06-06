from rest_framework import serializers


class ReceiptRequestSerializer(
    serializers.Serializer
):

    payment_id = serializers.IntegerField()

    def validate_payment_id(
        self,
        value
    ):

        if value <= 0:

            raise serializers.ValidationError(
                "Invalid payment id."
            )

        return value