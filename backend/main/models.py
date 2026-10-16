# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CallRequests(models.Model):
    id_request = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    comment = models.CharField(max_length=500, blank=True, null=True)
    request_date = models.DateTimeField()
    status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'call_requests'


class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField()
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    gender = models.CharField(max_length=10)
    registration_date = models.DateTimeField()
    email = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Doctor(models.Model):
    id_doctor = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    fisrt_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20)
    specialization = models.CharField(max_length=250)
    description = models.CharField(max_length=500, blank=True, null=True)
    experience = models.IntegerField()
    email = models.CharField(max_length=30)
    address = models.CharField(max_length=200, blank=True, null=True)
    diplomas = models.CharField(max_length=500, blank=True, null=True)
    photo = models.CharField(max_length=500, blank=True, null=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'doctor'


class ProductCategories(models.Model):
    id_category = models.AutoField(primary_key=True)
    id_category_parent = models.ForeignKey('self', models.DO_NOTHING, db_column='id_category_parent', blank=True, null=True)
    id_user = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_categories'


class Products(models.Model):
    id_product = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1500, blank=True, null=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    photo = models.CharField(max_length=500)
    id_category = models.ForeignKey(ProductCategories, models.DO_NOTHING, db_column='id_category')

    class Meta:
        managed = False
        db_table = 'products'


class Records(models.Model):
    id_record = models.AutoField(primary_key=True)
    id_service = models.ForeignKey('Services', models.DO_NOTHING, db_column='id_service')
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='id_client')
    id_doctor = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='id_doctor')
    id_request = models.OneToOneField(CallRequests, models.DO_NOTHING, db_column='id_request')
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    status = models.CharField(max_length=50)
    date_time = models.DateTimeField(db_column='date&time')  # Field renamed to remove unsuitable characters.
    comment = models.CharField(max_length=500, blank=True, null=True)
    payment_stat = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'records'


class RecordsBackupBeforeSeasonality(models.Model):
    id_record = models.IntegerField(blank=True, null=True)
    id_service = models.IntegerField(blank=True, null=True)
    id_client = models.IntegerField(blank=True, null=True)
    id_doctor = models.IntegerField(blank=True, null=True)
    id_request = models.IntegerField(blank=True, null=True)
    id_user = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    date_time = models.DateTimeField(db_column='date&time', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    comment = models.CharField(max_length=500, blank=True, null=True)
    payment_stat = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'records_backup_before_seasonality'


class Reviews(models.Model):
    id_review = models.AutoField(primary_key=True)
    id_record = models.ForeignKey(Records, models.DO_NOTHING, db_column='id_record')
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    text = models.CharField(max_length=500, blank=True, null=True)
    rating = models.IntegerField()
    daterec = models.DateField(db_column='dateRec')  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'


class ServiceCategories(models.Model):
    id_category = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    name = models.CharField(max_length=80)
    type = models.CharField(max_length=50)
    id_category_parent = models.ForeignKey('self', models.DO_NOTHING, db_column='id_category_parent', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_categories'


class Services(models.Model):
    id_service = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    id_category = models.ForeignKey(ServiceCategories, models.DO_NOTHING, db_column='id_category')
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    duration = models.TimeField()
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'services'


class UsedProducts(models.Model):
    id_used = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    id_record = models.ForeignKey(Records, models.DO_NOTHING, db_column='id_record')
    id_product = models.ForeignKey(Products, models.DO_NOTHING, db_column='id_product')
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'used_products'


class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    ip_user = models.IntegerField()
    last_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
