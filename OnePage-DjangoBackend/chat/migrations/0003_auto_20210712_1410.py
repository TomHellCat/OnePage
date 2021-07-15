# Generated by Django 3.0.7 on 2021-07-12 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20210711_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='website',
            name='messages',
        ),
        migrations.AddField(
            model_name='message',
            name='website',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.Website'),
        ),
    ]