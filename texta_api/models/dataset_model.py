from django.db import models
from .datarow_model import Datarow
from ..helpers.helpers import row_indexes_to_list
import json


class Dataset(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    rows = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.rows)

    def is_unique(name):
        return not Dataset.objects.filter(name=name).exists()

    def get_rows(self):
        rows = {}
        row_ids = row_indexes_to_list(self.rows)
        for row_id in row_ids:
            rows[row_id] = json.loads(Datarow.objects.get(pk=row_id).content, encoding='utf8')
        return rows

    def has_rows(self):
        return len(row_indexes_to_list(self.rows)) != 0