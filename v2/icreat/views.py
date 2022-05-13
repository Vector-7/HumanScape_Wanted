from datetime import datetime, timedelta

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from .serializers import IcreatSerializer
from .models import IcreatV2



class SubjectDetailView(RetrieveUpdateDestroyAPIView):
    '''
        작성자 : 남기윤, 하정현
    '''
    model = IcreatV2
    serializer_class = IcreatSerializer

    def get_queryset(self):
        res = IcreatV2.objects.all()
        return res


    def get(self, request, pk):
        return self.retrieve(request, pk)

    def patch(self, request, pk):
        return self.update(request, pk, partial = True)

    def delete(self, request, pk):
        """
        is_active가 False로 처리되어야 한다.
        """
        obj = get_object_or_404(IcreatV2, id=pk)
        if not obj.is_active:
            # 이미 삭제처리됨
            return Response({"error": "already deleted"}, status=status.HTTP_400_BAD_REQUEST)
        obj.is_active = False
        obj.save()
        return Response({"is_active": obj.is_active}, status=status.HTTP_204_NO_CONTENT)

class SubjectListView(ListCreateAPIView): #/api/v2/icreat/list
    model = IcreatV2
    serializer_class = IcreatSerializer

    def get_queryset(self):
        page = self.request.GET.get('page',1)
        pagesize = 10
        limit = pagesize * page
        offset = limit -pagesize
        a_week_ago = datetime.today() - timedelta(days = 7)
        subjects = IcreatV2.objects.filter(modified_at__gte=a_week_ago)[offset:limit]
        return subjects
