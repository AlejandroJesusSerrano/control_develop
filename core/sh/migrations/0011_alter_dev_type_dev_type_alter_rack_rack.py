# Generated by Django 5.0.6 on 2024-09-10 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh', '0010_dependency_edifice_alter_dependency_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dev_type',
            name='dev_type',
            field=models.CharField(max_length=50, unique=True, verbose_name='Tipo de Dispositivo'),
        ),
        migrations.AlterField(
            model_name='rack',
            name='rack',
            field=models.CharField(max_length=6, unique=True, verbose_name='Rack'),
        ),
    ]