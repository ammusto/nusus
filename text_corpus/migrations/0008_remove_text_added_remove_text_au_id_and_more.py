# Generated by Django 4.0.6 on 2022-08-03 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_corpus', '0007_remove_text_gen_id_text_genre_text_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='added',
        ),
        migrations.RemoveField(
            model_name='text',
            name='au_id',
        ),
        migrations.RemoveField(
            model_name='text',
            name='avail_read',
        ),
        migrations.RemoveField(
            model_name='text',
            name='descr',
        ),
        migrations.RemoveField(
            model_name='text',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='text',
            name='pdf',
        ),
        migrations.RemoveField(
            model_name='text',
            name='perm',
        ),
        migrations.RemoveField(
            model_name='text',
            name='permbib',
        ),
        migrations.RemoveField(
            model_name='text',
            name='pg_len',
        ),
        migrations.RemoveField(
            model_name='text',
            name='pg_rng',
        ),
        migrations.RemoveField(
            model_name='text',
            name='published_date',
        ),
        migrations.RemoveField(
            model_name='text',
            name='source',
        ),
        migrations.RemoveField(
            model_name='text',
            name='title_ar',
        ),
        migrations.RemoveField(
            model_name='text',
            name='title_tl',
        ),
        migrations.RemoveField(
            model_name='text',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='text',
            name='word_len',
        ),
    ]
