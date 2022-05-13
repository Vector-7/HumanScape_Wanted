from django.db import models


class BatchLog(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_count = models.IntegerField(default=0)
    updated_count = models.IntegerField(default=0)
    created_list = models.TextField(null=True, blank=True)
    updated_list = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'batch_log'
