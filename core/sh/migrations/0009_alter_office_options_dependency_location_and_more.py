# Generated by Django 5.0.6 on 2024-09-09 16:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sh', '0008_alter_office_loc_options_alter_office_loc_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='office',
            options={'ordering': ['id'], 'verbose_name': 'Oficina', 'verbose_name_plural': 'Oficinas'},
        ),
        migrations.AddField(
            model_name='dependency',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sh.location', verbose_name='Localidad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='office',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descripcion'),
        ),
    ]