# Generated by Django 5.0.6 on 2024-07-18 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('image', '0002_alter_image_user'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=10)),
                ('item_concept', models.CharField(max_length=15)),
                ('item_category', models.CharField(max_length=10)),
                ('maintext', models.CharField(max_length=150)),
                ('servetext', models.CharField(default='Default serve text', max_length=100)),
                ('maintext2', models.CharField(blank=True, max_length=150, null=True)),
                ('servetext2', models.CharField(blank=True, max_length=100, null=True)),
                ('add_information', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('image_id', models.ForeignKey(db_column='image_id', on_delete=django.db.models.deletion.CASCADE, to='image.image')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interaction_data', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image.image')),
            ],
        ),
    ]
