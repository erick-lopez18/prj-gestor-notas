# Generated by Django 4.2.1 on 2023-06-05 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_notes', '0003_alter_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='evento',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_notes.usuario'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_notes.usuario'),
        ),
    ]