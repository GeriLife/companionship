from rest_framework import serializers

from circles.models import Circle
from .models import Activity


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    circle = serializers.HyperlinkedRelatedField(view_name='circle-detail', read_only=True)
    participants = serializers.HyperlinkedRelatedField(many=True, view_name='companion-detail', read_only=True)
    organizers = serializers.HyperlinkedRelatedField(many=True, view_name='student-detail', read_only=True)

    class Meta:
        model = Activity
        fields = ('url', 'id', 'activity_type', 'activity_date', 'note', 'circle', 'participants', 'done', 'organizers')
