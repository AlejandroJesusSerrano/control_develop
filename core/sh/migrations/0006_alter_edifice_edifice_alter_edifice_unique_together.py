# Generated by Django 5.0.6 on 2024-09-02 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh', '0005_alter_brand_brand_alter_edifice_edifice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edifice',
            name='edifice',
            field=models.CharField(max_length=50, verbose_name='Edificio'),
        ),
        migrations.AlterUniqueTogether(
            name='edifice',
            unique_together={('location', 'edifice')},
        ),
    ]