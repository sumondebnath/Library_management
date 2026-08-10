from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_useraccount_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='user_type',
            field=models.CharField(blank=True, choices=[('Student', 'Student'), ('Other', 'Other')], default='', max_length=10),
        ),
    ]
