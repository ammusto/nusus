# Generated by Django 4.0.6 on 2022-08-04 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_corpus', '0012_rename_topic_text_style_remove_text_avail_read_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='added',
        ),
        migrations.RemoveField(
            model_name='text',
            name='published_date',
        ),
    ]
