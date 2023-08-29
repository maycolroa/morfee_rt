# Generated by Django 4.2.4 on 2023-08-28 19:49

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMorfee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AuthCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('correo', models.CharField(max_length=100)),
                ('contacto', models.CharField(max_length=30)),
                ('is_indigena', models.BooleanField()),
            ],
            options={
                'db_table': 'auth_cliente',
            },
        ),
        migrations.CreateModel(
            name='AuthRol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(max_length=20)),
                ('nivel', models.IntegerField()),
            ],
            options={
                'db_table': 'auth_rol',
            },
        ),
        migrations.CreateModel(
            name='Diccionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modulo', models.CharField(max_length=30)),
                ('coleccion', models.CharField(max_length=50, unique=True)),
                ('alias', models.CharField(max_length=50)),
                ('campos', models.CharField(max_length=700)),
                ('has_data', models.IntegerField(default=0)),
                ('type_head', models.CharField(choices=[('auto', 'Auto'), ('file_parse', 'File Parse'), ('file_fixed', 'File Fixed'), ('file_free', 'File Free')], default='file_free', max_length=10)),
                ('propietario', models.CharField(choices=[('Morfee', 'Morfee'), ('Cliente', 'Cliente')], default='Cliente', max_length=10)),
                ('reglas', models.CharField(blank=True, default='', max_length=200)),
                ('tipo', models.CharField(default='final', max_length=10)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.authcliente')),
            ],
            options={
                'db_table': 'diccionario',
            },
        ),
        migrations.CreateModel(
            name='ControlImportBasic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campos', models.CharField(max_length=500, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('coleccion', models.CharField(blank=True, default='', max_length=50)),
                ('total', models.IntegerField(default=0)),
                ('clave', models.CharField(max_length=20, null=True)),
                ('estado', models.CharField(max_length=10, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.authcliente')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'control_import_basic',
            },
        ),
        migrations.AddField(
            model_name='usermorfee',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.authcliente'),
        ),
        migrations.AddField(
            model_name='usermorfee',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usermorfee',
            name='rol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.authrol'),
        ),
        migrations.AddField(
            model_name='usermorfee',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
