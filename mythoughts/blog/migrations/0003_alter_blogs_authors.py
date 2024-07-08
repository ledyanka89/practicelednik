# Generated by Django 4.2.13 on 2024-07-08 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('blog', '0002_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='authored_blogs', to='users.users'),
        ),
    ]
