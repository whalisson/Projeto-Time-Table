# Generated by Django 5.0.6 on 2024-06-23 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mm1', '0003_instructor_available_times_alter_meetingtime_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='available_times',
            field=models.ManyToManyField(blank=True, to='mm1.meetingtime'),
        ),
    ]