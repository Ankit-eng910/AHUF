from rest_framework import serializers
from .hashid_util import encode_id

class HashedIdMixin(serializers.ModelSerializer):
    encoded_id = serializers.SerializerMethodField()

    def get_encoded_id(self, obj):
        return encode_id(obj.id)