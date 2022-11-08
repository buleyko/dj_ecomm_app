# Generated by Django 4.1.2 on 2022-11-08 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnd', '0002_alter_delivery_name_alter_fnd_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='fnd',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fnd',
            name='alias',
            field=models.SlugField(max_length=180, unique=True),
        ),
    ]
