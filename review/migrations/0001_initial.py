# Generated by Django 4.2.19 on 2025-02-17 05:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('performance', '0002_alter_genre_options_alter_performance_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('content', models.CharField(max_length=280, verbose_name='리뷰 내용')),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='performance.performance', verbose_name='공연')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'verbose_name': '후기',
                'verbose_name_plural': '후기',
                'db_table': 'review',
                'ordering': ['-created_at'],
            },
        ),
    ]
