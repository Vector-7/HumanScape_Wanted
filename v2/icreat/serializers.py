from rest_framework import serializers
from .models import Icreat

class IcreatSerializer(serializers.ModelSerializer):
    '''
    작성자 : 남기윤, 하정현
    '''
    class Meta:
        model = Icreat
        fields = (
            "subject","sub_num","period","boundary",
            "remark","institute","trial","goal_research",
            "meddept","is_active"
            )

    def update(self, instance, data):
        # update시 is_active 수정 불가
        if 'is_active' in data:
            raise serializers.ValidationError("You can't modify is_active")
        return super().update(instance, data)