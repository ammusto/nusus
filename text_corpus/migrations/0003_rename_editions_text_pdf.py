# Generated by Django 4.0.6 on 2022-07-30 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_corpus', '0002_remove_author_bio_ar_remove_author_books_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='text',
            old_name='editions',
            new_name='pdf',
        ),
    ]
