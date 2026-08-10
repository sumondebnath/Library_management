from django.db import migrations


def create_missing_accounts(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserAccount = apps.get_model('accounts', 'UserAccount')
    for user in User.objects.all():
        UserAccount.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_useraccount_gender_user_type'),
    ]

    operations = [
        migrations.RunPython(create_missing_accounts),
    ]
