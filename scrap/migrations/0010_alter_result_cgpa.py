# Generated by Django 5.1.4 on 2025-01-18 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0009_alter_result_re_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='cgpa',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
