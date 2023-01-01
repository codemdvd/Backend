from django.db import models
from django.contrib.auth.models import AbstractUser


    
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


class Cars(models.Model):
    car_id = models.IntegerField(primary_key=True)
    car_vin_code = models.CharField(max_length=30)
    car_brand = models.CharField(max_length=20)
    engine_type = models.CharField(max_length=30)
    client = models.ForeignKey('Client', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cars'


class Client(models.Model):
    client_id = models.IntegerField(primary_key=True)
    client_name = models.CharField(max_length=100)
    client_ph_number = models.CharField(max_length=17)
    client_email = models.CharField(max_length=40, blank=True, null=True)
    personal_discount = models.FloatField(blank=True, null=True, db_column="personal_discount")
    car = models.SmallIntegerField(blank=True,null=True,db_column="cars" )

    class Meta:
        managed = False
        db_table = 'client'


class DeliveryClassifier(models.Model):
    delivery_code = models.SmallIntegerField(primary_key=True)
    delivery_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'delivery_classifier'


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


class Employee(models.Model):
    emp_id = models.SmallIntegerField(primary_key=True)
    emp_name = models.CharField(max_length=100)
    emp_login = models.CharField(max_length=20)
    emp_password = models.CharField(max_length=50)
    emp_ph_number = models.CharField(max_length=17)
    role_code = models.ForeignKey('RoleClassifier', models.DO_NOTHING, db_column='role_code')

    class Meta:
        managed = False
        db_table = 'employee'
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'


    def __str__(self):
        return self.emp_login



class Income(models.Model):
    income_id = models.IntegerField(primary_key=True)
    sending_date = models.DateField()
    recieving_date = models.DateField(blank=True, null=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'income'


class IncomeProduct(models.Model):
    amount = models.SmallIntegerField()
    product = models.OneToOneField('Product', models.DO_NOTHING, primary_key=True)
    income = models.ForeignKey(Income, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'income_product'
        unique_together = (('product', 'income'),)


class OrderProduct(models.Model):
    order = models.OneToOneField('OrderTable', models.DO_NOTHING, primary_key=True)
    product = models.ForeignKey('Product', models.DO_NOTHING)
    amount = models.SmallIntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_product'
        unique_together = (('order', 'product'),)


class OrderStausClassifier(models.Model):
    ord_status_code = models.SmallIntegerField(primary_key=True)
    ord_stat_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'order_staus_classifier'

    # def  __str__(self):
    #     return self.ord_status_code


class OrderTable(models.Model):
    order_id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=150)
    total_price = models.DecimalField(max_digits=100, decimal_places=2)
    client = models.ForeignKey(Client, models.DO_NOTHING)
    ord_status_code = models.ForeignKey(OrderStausClassifier, models.DO_NOTHING, db_column='ord_status_code')
    delivery_code = models.ForeignKey(DeliveryClassifier, models.DO_NOTHING, db_column='delivery_code')
    executor = models.ForeignKey(Employee, models.DO_NOTHING)
    payment_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_table'


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=200)
    sets_left = models.SmallIntegerField()
    detail_number = models.CharField(max_length=30)
    brand = models.CharField(max_length=30, blank=True, null=True)
    product_price = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class RoleClassifier(models.Model):
    role_code = models.SmallIntegerField(primary_key=True)
    role_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role_classifier'
