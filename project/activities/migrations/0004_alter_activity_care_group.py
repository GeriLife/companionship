# Generated by Django 4.0 on 2021-12-28 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('care_groups', '0002_caregroup_members'),
        ('activities', '0003_activity_care_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='care_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='care_groups.caregroup'),
        ),
    ]