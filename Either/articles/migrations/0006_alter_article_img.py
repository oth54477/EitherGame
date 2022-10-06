# Generated by Django 3.2.13 on 2022-10-06 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_alter_article_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.URLField(default='data:image/jpeg;base64,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', max_length=1000),
        ),
    ]
