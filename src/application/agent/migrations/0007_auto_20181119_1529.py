# Generated by Django 2.1 on 2018-11-19 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_tasksexecution_comments'),
        ('agent', '0006_store_inn'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='Count')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.Good', verbose_name='Good')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.Store', verbose_name='For store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.User', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Cart item',
                'verbose_name_plural': 'Cart',
                'db_table': 'agent_cart',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='ordergood',
            name='count',
            field=models.IntegerField(default=1, verbose_name='Count'),
        ),
    ]
