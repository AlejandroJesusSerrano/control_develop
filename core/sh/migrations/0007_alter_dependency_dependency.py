# Generated by Django 5.0.6 on 2024-09-02 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh', '0006_alter_edifice_edifice_alter_edifice_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependency',
            name='dependency',
            field=models.CharField(max_length=75, unique=True, verbose_name='Dependencia'),
        ),
    ]
