# Generated by Django 5.0.6 on 2024-06-24 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_post_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default='2003-09-09'),
            preserve_default=False,
        ),
    ]
