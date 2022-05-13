from django.db import models


class IcreatV2(models.Model):
    trial_id = models.CharField(max_length=20, unique=True, verbose_name='CRIS등록번호')
    scientific_title_kr = models.TextField(verbose_name='연구제목 국문')
    scientific_title_en = models.TextField(verbose_name='연구제목 영문')
    date_registration = models.DateTimeField(verbose_name='연구등록일',blank=True)
    date_updated = models.DateTimeField(verbose_name='최종갱신일',blank=True)
    date_enrolment = models.DateTimeField(verbose_name='첫 연구대상자 등록일',blank=True)
    type_enrolment_kr = models.CharField(max_length=30, verbose_name='첫 연구대상자 등록여부 국문', blank=True)
    results_date_completed = models.DateTimeField(verbose_name='연구종료일',blank=True)
    results_type_date_completed_kr = models.CharField(max_length=30, verbose_name='연구종료일/ 상태 국문', blank=True)
    study_type_kr = models.CharField(max_length=40,verbose_name='연구종류 국문', blank=True)
    i_freetext_kr = models.TextField(verbose_name='중재종류 국문', blank=True)
    phase_kr = models.CharField(max_length=100, verbose_name='임상시험단계 국문', blank=True)
    source_name_kr = models.CharField(max_length=200, verbose_name='연구비지원 기관명 국문', blank=True)
    primary_sponsor_kr = models.CharField(max_length=200, verbose_name='연구책임 기관명 국문', blank=True)
    primary_outcome_1_kr = models.TextField(verbose_name='주요결과변수 1 국문', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'icreat_v2'