from rest_framework import viewsets

from api.models import Brother
from api.serializers import BrotherSerializer


# ViewSets define the view behavior.
class BrotherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brother.objects.all()
    serializer_class = BrotherSerializer
