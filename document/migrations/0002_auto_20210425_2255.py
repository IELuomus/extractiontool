# Generated by Django 3.1.6 on 2021-04-25 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pdf',
            old_name='file',
            new_name='filex',
        ),
    ]
