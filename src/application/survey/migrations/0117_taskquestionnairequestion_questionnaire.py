# Generated by Django 2.2.24 on 2021-08-02 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0116_remove_taskquestionnaire_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskquestionnairequestion',
            name='questionnaire',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='survey_taskquestionnairequestion_task', to='survey.TaskQuestionnaire', verbose_name='Questionnaire'),
            preserve_default=False,
        ),
    ]