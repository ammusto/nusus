# Generated by Django 4.0.6 on 2022-09-27 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_corpus', '0006_rename_mbio_teammem_bio_rename_mname_teammem_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammem',
            name='website',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
