# Generated by Django 4.0.6 on 2022-09-26 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_corpus', '0002_alter_corpusup_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMem',
            fields=[
                ('mem_id', models.IntegerField(primary_key=True, serialize=False)),
                ('mname', models.CharField(max_length=40)),
                ('mbio', models.TextField()),
                ('mphoto', models.ImageField(upload_to='mem')),
            ],
        ),
    ]
