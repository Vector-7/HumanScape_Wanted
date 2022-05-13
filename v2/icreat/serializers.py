from rest_framework import serializers
from .models import IcreatV2

class IcreatV2Serializer(serializers.ModelSerializer):
    '''
    작성자 : 남기윤
    '''
    date_registration = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    date_updated = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    date_enrolment = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    results_date_completed = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = IcreatV2
        fields = (
            "trial_id","scientific_title_kr","scientific_title_en","date_registration",
            "date_updated","date_enrolment","type_enrolment_kr","results_date_completed",
            "results_type_date_completed_kr","study_type_kr","i_freetext_kr",
            "phase_kr","source_name_kr","primary_sponsor_kr","primary_outcome_1_kr"
            )

    def update(self, instance, data):
        # update시 is_active 수정 불가
        if 'is_active' in data:
            raise serializers.ValidationError("You can't modify is_active")
        return super().update(instance, data)
