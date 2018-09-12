from rest_framework import serializers

from wazimap_health.models import (PublicHealthFacilities,
                                   PublicHealthServices,
                                   PrivatePharmacies,
                                   PharmacyServices)


class PublicHealthFacilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicHealthFacilities
        fields = '__all__'


class PharmacySerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivatePharmacies
        fields = '__all__'


# class ServicesModelSerializer(serializers.ModelSerializer):
#     def __init__(self, *args, **kwargs):
#         super(ServicesModelSerializer, self).__init__(*args, **kwargs)

#         if 'lables' in self.fields:
#             raise RuntimeError('No labels allowed in this serializer')
#         self.fields['lables'] = serializers.SerializerMethodField()

#     def get_lables(self, args):
#         labels = {}
#         for field in self.Meta.model._meta.get_fields():
#             if field.name in self.fields:
#                 labels[field.name] = field.verbose_name
#         return labels

# class PublicServicesSerializer(ServicesModelSerializer):
#     class Meta:
#         model = PublicHealthServices
#         fields = '__all__'
