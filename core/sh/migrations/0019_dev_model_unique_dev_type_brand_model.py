# Generated by Django 5.0.6 on 2024-10-01 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh', '0018_alter_dependency_dependency_alter_office_office_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='dev_model',
            constraint=models.UniqueConstraint(fields=('dev_type', 'brand', 'dev_model'), name='unique_dev_type_brand_model'),
        ),
    ]
