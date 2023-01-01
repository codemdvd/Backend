from .models import Product, Employee, OrderTable, OrderProduct, RoleClassifier
from django.forms import ModelForm, TextInput, DateInput, EmailField, PasswordInput, NumberInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


class OrderForm(ModelForm):
    class Meta:
        model = OrderTable

        fields = '__all__'
        widgets = {
            "order_id": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер заказа'
            }),
             "address": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес'
            }),
             "total_price": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Стоимость заказа'
            }),
             "client": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID клиента'
            }),
             "ord_status_code": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Код статуса'
            }),
             "delivery_code": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Код доставки'
            }),
             "executor": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID исполнителя'
            }),
             "payment_date": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата оплаты'
            }),
                }
class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = [
            'emp_id',
            'emp_name',
            'emp_login',
            'emp_password',
            'emp_ph_number',
            'role_code'
        ]
        widgets = {
            "emp_id": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID сотрудника'
            }),
            "emp_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя сотрудника'
            }),
            "emp_login": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин'
            }),
            "emp_password": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }),
            "emp_ph_number": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона'
            }),
            "role_code": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Код роли'
            }),

        }
class OrderProductForm(ModelForm):
    class Meta:
        model = OrderProduct
        fields = '__all__'
        widgets = {
            "order": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер заказа'
            }),
            "product": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер детали'
            }),
            "amount": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество комплектов'
            }),
            "discount": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Скидка'
            }),
        }
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', \
    widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', \
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', \
    widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', \
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', \
    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']





        