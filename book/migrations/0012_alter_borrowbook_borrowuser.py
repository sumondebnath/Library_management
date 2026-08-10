import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_alter_borrowbook_borrowuser'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowbook',
            name='borrowUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowed_books', to=settings.AUTH_USER_MODEL),
        ),
    ]
