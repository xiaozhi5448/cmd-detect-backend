# Generated by Django 3.1.2 on 2020-10-12 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misalarm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='misalarmcommand',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]