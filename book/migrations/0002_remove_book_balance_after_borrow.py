# Generated by Django 5.0.1 on 2024-02-04 02:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='balance_after_borrow',
        ),
    ]
