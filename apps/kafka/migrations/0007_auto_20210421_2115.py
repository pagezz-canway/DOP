# Generated by Django 2.2.6 on 2021-04-21 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kafka', '0006_auto_20210421_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kafkabroker',
            name='ip_port',
            field=models.CharField(default='', max_length=50, unique=True, verbose_name='节点ip'),
        ),
    ]