# Generated by Django 4.0.6 on 2022-10-16 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_corpus', '0016_text_contrib'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='coins',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
