from django.db import models


class AIProblem(models.Model):

    te_id = models.IntegerField('Идентификатор выполненной задачи')

    class Meta:
        db_table = 'ai_problems'
        ordering = ['id']
        verbose_name = 'Проблема распознавания'
        verbose_name_plural = 'Проблемы распознавания'


class AIProject(models.Model):

    name = models.CharField('Название', max_length=100, unique=True)
    is_default = models.BooleanField('По умолчанию', default=False)

    class Meta:
        db_table = 'ai_projects'
        ordering = ['name', 'id']
        verbose_name = 'Проект распознавания'
        verbose_name_plural = 'Проекты распознавания'

    def __str__(self):
        return self.name
