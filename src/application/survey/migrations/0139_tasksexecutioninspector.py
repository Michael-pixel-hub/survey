# Generated by Django 2.2.24 on 2021-08-09 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0138_tasksexecutionassortment_constructor_step_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TasksExecutionInspector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('constructor_step_name', models.CharField(default='', max_length=200, verbose_name='Step name')),
                ('inspector_upload_images_text', models.TextField(blank=True, default='', verbose_name='Upload images message')),
                ('inspector_error', models.TextField(blank=True, default='', null=True, verbose_name='Error text')),
                ('inspector_recognize_text', models.TextField(blank=True, default='', null=True, verbose_name='Recognize message')),
                ('inspector_report_text', models.TextField(blank=True, default='', null=True, verbose_name='Report')),
                ('inspector_positions_text', models.TextField(blank=True, default='', null=True, verbose_name='Positions text')),
                ('inspector_status', models.CharField(choices=[('undefined', 'Undefined'), ('wait', 'Waiting for inspector'), ('upload_wait', 'Upload wait'), ('upload_error', 'Upload error'), ('parse_error', 'Parse error'), ('report_process', 'Report process'), ('report_error', 'Report error'), ('report_wait', 'Report waiting'), ('error', 'Error'), ('success', 'Success parsing')], default='wait', max_length=20, verbose_name='Inspector status')),
                ('inspector_report_id', models.IntegerField(blank=True, null=True, verbose_name='Report id')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_tasksexecutioninspector_task', to='survey.TasksExecution', verbose_name='Task execution')),
            ],
            options={
                'verbose_name': 'Task execution inspector',
                'verbose_name_plural': 'Tasks execution inspector',
                'db_table': 'chl_tasks_executions_inspector',
                'ordering': ['-task__date_start', 'id'],
            },
        ),
    ]