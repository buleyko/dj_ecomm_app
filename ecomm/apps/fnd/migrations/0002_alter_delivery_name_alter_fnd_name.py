# Generated by Django 4.1.2 on 2022-11-08 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fnd', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.JSONField(help_text='Required'),
        ),
        migrations.AlterField(
            model_name='fnd',
            name='name',
            field=models.JSONField(blank=True, null=True),
        ),
    ]