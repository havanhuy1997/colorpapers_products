# Generated by Django 3.2.1 on 2021-05-05 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20210505_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processexecutions',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('running', 'running'), ('completed', 'completed')], default='pending', help_text='Text Choice Field, 50, Characters.', max_length=50, verbose_name='Execution Status'),
        ),
    ]
