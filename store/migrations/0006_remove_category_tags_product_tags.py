# Generated by Django 5.1.1 on 2024-10-24 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_category_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='tags',
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='store.tag'),
        ),
    ]
