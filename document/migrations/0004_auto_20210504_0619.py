# Generated by Django 3.1.6 on 2021-05-04 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0003_documenttask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttask',
            name='status',
            field=models.CharField(choices=[('N/A', 'Na'), ('Waiting', 'Waiting'), ('Running', 'Running'), ('Finished', 'Finished')], max_length=32),
        ),
    ]
