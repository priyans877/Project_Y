# Generated by Django 5.1.4 on 2025-01-18 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0008_rename_result_result_result_s'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='re_count',
            field=models.CharField(max_length=50),
        ),
    ]
