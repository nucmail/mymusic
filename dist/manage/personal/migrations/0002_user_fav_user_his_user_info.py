# Generated by Django 2.2.10 on 2022-01-05 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_fav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=200, verbose_name='user_id')),
                ('song_id', models.CharField(max_length=200, verbose_name='song_id')),
            ],
        ),
        migrations.CreateModel(
            name='user_his',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=200, verbose_name='user_id')),
                ('song_id', models.CharField(max_length=200, verbose_name='song_id')),
                ('p', models.IntegerField(default='')),
                ('fractional_play_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('user_id', models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='user_id')),
                ('user_name', models.CharField(max_length=200, verbose_name='user_name')),
                ('user_email', models.EmailField(max_length=254, verbose_name='user_email')),
                ('user_phone', models.CharField(max_length=200, verbose_name='user_email')),
            ],
        ),
    ]
