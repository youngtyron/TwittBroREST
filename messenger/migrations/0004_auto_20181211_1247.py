# Generated by Django 2.1.3 on 2018-12-11 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0003_auto_20181130_1348'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'get_latest_by': 'pub_date', 'ordering': ['pub_date'], 'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
    ]