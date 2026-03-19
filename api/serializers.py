from rest_framework import serializers
from api.models import Brother


class BrotherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brother
        fields = ['id', 'full_name', 'big_brother', 'initiation_term', 'major']

    def to_representation(self, instance: Brother):
        representation = super().to_representation(instance)

        representation["big_brother"] = (
            instance.big_brother.id if instance.big_brother else -1
        )
        return representation

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.accepted_renderer.format == "api":
            fields["url"] = serializers.HyperlinkedIdentityField(
                view_name="brother-detail"
            )

        return fields
