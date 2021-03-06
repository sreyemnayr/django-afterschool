# Generated by Django 2.1.1 on 2020-05-21 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20181106_0904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('temperature', models.DecimalField(decimal_places=1, default=98.6, max_digits=6)),
                ('result', models.SmallIntegerField(choices=[(0, 'Cleared'), (1, 'Denied Entry'), (2, 'Isolated')])),
            ],
            options={
                'verbose_name': 'scan',
                'verbose_name_plural': 'scans',
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.AddField(
            model_name='scan',
            name='scanner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='records', to='students.Staff'),
        ),
        migrations.AddField(
            model_name='scan',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scans', to='students.Staff'),
        ),
        migrations.AddField(
            model_name='scan',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scans', to='students.Student'),
        ),
    ]
