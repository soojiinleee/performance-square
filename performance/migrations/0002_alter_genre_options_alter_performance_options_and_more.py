# Generated by Django 4.2.19 on 2025-02-17 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("performance", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="genre",
            options={"verbose_name": "장르", "verbose_name_plural": "장르"},
        ),
        migrations.AlterModelOptions(
            name="performance",
            options={
                "ordering": ["ended_at"],
                "verbose_name": "공연",
                "verbose_name_plural": "공연",
            },
        ),
        migrations.AlterField(
            model_name="genre",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="performance",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
