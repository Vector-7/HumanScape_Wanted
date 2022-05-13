from django.db import models


class Icreat(models.Model): 
    subject = models.TextField(verbose_name='과제명')
    sub_num = models.CharField(max_length=100, unique=True, verbose_name='과제번호')
    period = models.CharField(max_length=20, verbose_name='연구기간', blank=True)
    boundary = models.CharField(max_length=50, verbose_name='연구범위')
    remark = models.CharField(max_length=100, verbose_name='연구종류')
    institute = models.CharField(max_length=100, verbose_name='연구책임기관')
    trial = models.CharField(max_length=100, verbose_name='임상시험단계(연구모형)', blank=True)
    goal_research = models.CharField(max_length=20, verbose_name='전체목표연구대상자수', blank=True)
    meddept = models.CharField(max_length=100, verbose_name='진료과')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'icreat'
        indexes = (models.Index(fields=('sub_num',), name='sub_num_idx'), )
