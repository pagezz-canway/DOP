# Generated by Django 2.2.6 on 2021-05-08 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('globalview', '0002_taskrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskrecord',
            name='task_mode',
            field=models.IntegerField(choices=[(0, '同步触发'), (1, '异步触发')], default=1, verbose_name='任务模式'),
        ),
    ]