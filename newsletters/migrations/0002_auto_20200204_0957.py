# Generated by Django 3.0.2 on 2020-02-04 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewsletterUsers',
            new_name='NewsletterUser',
        ),
    ]
