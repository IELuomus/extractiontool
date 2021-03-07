# Generated by Django 3.1.6 on 2021-03-07 19:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_id', models.IntegerField(db_index=True)),
                ('line_id', models.IntegerField(db_index=True)),
                ('paragraph_id', models.IntegerField(db_index=True)),
                ('block_id', models.IntegerField(db_index=True)),
                ('page_id', models.IntegerField(db_index=True)),
                ('document_id', models.IntegerField(db_index=True)),
                ('vasen', models.IntegerField(db_index=True)),
                ('top', models.IntegerField(db_index=True)),
                ('width', models.IntegerField(db_index=True)),
                ('height', models.IntegerField(db_index=True)),
                ('conf', models.IntegerField(db_index=True)),
                ('text', models.CharField(db_index=True, max_length=200)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'tes_word',
                'managed': True,
                'unique_together': {('word_id', 'line_id', 'paragraph_id', 'block_id', 'page_id', 'document_id')},
            },
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paragraph_id', models.IntegerField(db_index=True)),
                ('block_id', models.IntegerField(db_index=True)),
                ('page_id', models.IntegerField(db_index=True)),
                ('document_id', models.IntegerField(db_index=True)),
                ('vasen', models.IntegerField(db_index=True)),
                ('top', models.IntegerField(db_index=True)),
                ('width', models.IntegerField(db_index=True)),
                ('height', models.IntegerField(db_index=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'tes_paragraph',
                'managed': True,
                'unique_together': {('paragraph_id', 'block_id', 'page_id', 'document_id')},
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.IntegerField(db_index=True)),
                ('document_id', models.IntegerField(db_index=True)),
                ('vasen', models.IntegerField(db_index=True)),
                ('top', models.IntegerField(db_index=True)),
                ('width', models.IntegerField(db_index=True)),
                ('height', models.IntegerField(db_index=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'tes_page',
                'managed': True,
                'unique_together': {('page_id', 'document_id')},
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_id', models.IntegerField(db_index=True)),
                ('paragraph_id', models.IntegerField(db_index=True)),
                ('block_id', models.IntegerField(db_index=True)),
                ('page_id', models.IntegerField(db_index=True)),
                ('document_id', models.IntegerField(db_index=True)),
                ('vasen', models.IntegerField(db_index=True)),
                ('top', models.IntegerField(db_index=True)),
                ('width', models.IntegerField(db_index=True)),
                ('height', models.IntegerField(db_index=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'tes_line',
                'managed': True,
                'unique_together': {('line_id', 'paragraph_id', 'block_id', 'page_id', 'document_id')},
            },
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_id', models.IntegerField(db_index=True)),
                ('page_id', models.IntegerField(db_index=True)),
                ('document_id', models.IntegerField(db_index=True)),
                ('vasen', models.IntegerField(db_index=True)),
                ('top', models.IntegerField(db_index=True)),
                ('width', models.IntegerField(db_index=True)),
                ('height', models.IntegerField(db_index=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'tes_block',
                'managed': True,
                'unique_together': {('block_id', 'page_id', 'document_id')},
            },
        ),
    ]
