# Generated by Django 4.2.7 on 2023-11-24 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='document_manager.folder'),
        ),
    ]
