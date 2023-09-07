from django.db import models
from datetime import date, datetime, time,timedelta


class data_entry(models.Model):
    date = models.DateTimeField()
    visitors = models.IntegerField()

    def __str__(self) -> str:
        return str(self.date)
