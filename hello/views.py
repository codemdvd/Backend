import re
import os
import mimetypes
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
from .models import *
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db import connection
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import logout


def choice(request):
    return render(request, "hello/choice.html")

def tasks(request):              
    return render(request, "hello/tasks.html")

def clients(request):
    search_query = request.GET.get('search', '')
    if search_query:
        client = Client.objects.filter(client_name__contains=search_query)
    else:
        client = Client.objects.all()

    return render(request, "hello/clients.html",{'client': client})

def new_emp(request, commit=True):
    error1= ''
    if request.method == 'POST':
        form1 = EmployeeForm(request.POST)

        if form1.is_valid():
            form_emp_id = form1.cleaned_data.get("emp_id")
            form_emp_name = f"'{form1.cleaned_data.get('emp_name')}'"
            form_emp_login = f"'{form1.cleaned_data.get('emp_login')}'"
            form_emp_password = f"'{form1.cleaned_data.get('emp_password')}'"
            form_emp_ph_number = f"'{form1.cleaned_data.get('emp_ph_number')}'"
            form_role_code = str(form1.cleaned_data.get('role_code'))
            search = re.search(r'\(\d{1,6}\)', form_role_code).group()[1:-1]
            search_to_int = int(search)
            with connection.cursor() as cursor:
                cursor.execute(f"CALL public.add_employee({form_emp_id}, \
                                                          {form_emp_name},\
                                                          {form_emp_login},\
                                                          {form_emp_password},\
                                                          {form_emp_ph_number},\
                                                          {search_to_int})")
            
            return redirect('register')
        else:
            error1 = 'Форма неверно заполенна'

    form1 = EmployeeForm()

    data1 = {
        'form': form1,
        'error': error1
    }
    users_in_group = Group.objects.get(name="Admin").user_set.all()
    if request.user in users_in_group:
        return render(request, "hello/new_emp.html", data1 )
    else:
        return render(request, "hello/permission.html")


def register(request):
    logistic = Group.objects.get(name="Logistics")
    employee = Group.objects.get(name="Employee")
    error = ''
    if request.method == 'POST':
        form2 = RegisterUserForm(request.POST)
        if form2.is_valid():
            new_user = form2.save(commit=False)
            new_user.set_password(form2.cleaned_data['password1'])
            new_user.save()
            print(new_user.username)
            if Employee.objects.filter(role_code = 2):
                        new_user.groups.add(employee)
            if Employee.objects.filter(role_code = 6):
                        new_user.groups.add(logistic)
            return redirect('employees')
        else:
            print(form2)
            error = 'Пароли не совпадают'

    form2 = RegisterUserForm()
    role = Employee.objects.all()
    

    data = {
        'form2': form2,
        'error': error
    }
    return render(request, "hello/register.html", data)


def new_task(request):
    error= ''
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_tasks')
        else:
            error = 'Форма неверно заполенна'
            print(form)
    form = OrderForm()
    data = {
        'form': form,
        'error': error
    }
    users_in_group = Group.objects.get(name="Employee").user_set.all()
    if request.user in users_in_group:
        return render(request, "hello/new_task.html", data)
    else:
        return render(request, "hello/permission.html")

def update_order(request):
    error= ''
    if request.method == 'POST':
        order_id = request.GET.get("order_id")
        order = OrderTable.objects.get(order_id = order_id)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('all_tasks')
        else:
            error = 'Форма неверно заполенна'
            print(form)
    if request.method == 'GET':
        if "order_id" in request.GET.keys():
            order_id = request.GET.get("order_id")
            order = OrderTable.objects.filter(order_id=order_id)[0]
            form = OrderForm(initial={
                'order_id': order.order_id,
                'address': order.address,
                'total_price': order.total_price,
                'client': order.client,
                'ord_status_code': order.ord_status_code,
                'delivery_code': order.delivery_code,
                'executor': order.executor,
                'payment_date': order.payment_date
            })



            return render(request,"hello/update_order.html",{'form':form})

    if request.user.is_authenticated:
        employee = Employee.objects.filter(role_code = 2)
        if employee:
            for el in employee:
                if el.emp_login == request.user.username:
                    employees = True


    form = OrderForm()

    data = {
        'form': form,
        'error': error
    }
    if employees == True:
        return render(request, "hello/update_order.html", data)
    else:
        return render(request, "hello/permission.html")


def all_tasks(request):
    search_query = request.GET.get('search', '')
    c = 0
    users_in_group2 = Group.objects.get(name="Admin").user_set.all()

    if search_query:
        if request.user.is_authenticated:
            if request.user not in users_in_group2:
                employee = Employee.objects.all()
                if employee:
                    for el in employee:
                        if el.emp_login == request.user.username:
                            cr1 = Q(executor = el.emp_id)
                            cr3 = Q(address__contains=search_query)
                            order = OrderTable.objects.filter(cr1  & cr3)
                            for el in order:
                                c += 1
            else:
                order = OrderTable.objects.all()
                for el in order:
                    c += 1
    else:
        if request.user.is_authenticated:
            if request.user not in users_in_group2:
                employee = Employee.objects.all()
                if employee:
                    for el in employee:
                        if el.emp_login == request.user.username:
                            order = OrderTable.objects.filter(executor = el.emp_id)
                            for el in order:
                                c += 1
                else:
                    return redirect('home')
            else:
                order = OrderTable.objects.all()    
                for el in order:
                    c += 1
        else:
            order = OrderTable.objects.all()
            return redirect('home')

    data = {
        'order' : order,
        'employee' : employee,
        'c' : c
    }
    employee = Employee.objects.all()
    users_in_group = Group.objects.get(name="Employee").user_set.all()
    if request.user in users_in_group:
        return render(request, "hello/all_tasks.html", data)
    else:
        return render(request, "hello/permission.html")

def order_product(request):
    order_id = request.GET.get("order_id")
    order_product = OrderProduct.objects.filter(order_id = order_id)
    data = {
        'order_product': order_product,
        'order_id': order_id
        }
    return render(request, "hello/order_product.html", data )

def status_classifier(request):
    status = OrderStausClassifier.objects.all()
    return render(request, "hello/status_classifier.html", {'status': status})

def delivery_classifier(request):
    delivery = DeliveryClassifier.objects.all()
    return render(request, "hello/delivery_classifier.html", {'delivery':delivery})

def new_order_product(request):
    error= ''
    if request.method == 'POST':
        form = OrderProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_tasks')
        else:
            error = 'Форма неверно заполенна'
            print(form)
    if request.method == 'GET':
        if "order_id" in request.GET.keys():
            order_id = request.GET.get("order_id")
            order = OrderTable.objects.filter(order_id=order_id)[0]
            form = OrderProductForm(initial={
                'order': order.order_id
            })

            return render(request,"hello/new_order_product.html",{'form':form})

    form = OrderProductForm()
    return render(request,"hello/new_order_product.html", {'error': error, 'form': form})


def hello_there(request):
    return render(
        request,
        'hello/hello_there.html',
    )

def detail_view(request):
    error1 = ''
    if request.method == "GET":
        query = request.GET.get('search')
        if query == '':
            query = 'None'
    error1 = 'Неверный запрос'

    data = {
    'query': query, 
    'tasks': tasks,
    'error1' : error1
    }
    return render(request, "hello/detail_view.html", data)

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name= 'hello/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))
    def get_success_url(self):
        return reverse_lazy('tasks')

def report(request):
    manager =  False
    if request.user.is_authenticated:
        employee = Employee.objects.filter(position = 3)
        if employee:
            for el in employee:
                if el.USERNAME_FIELD == request.user.username:
                    manager = True
    date1 = request.GET.get('date1', '')
    date2 = request.GET.get('date2', '')
    emp_id = request.GET.get('emp_id', '')
    if date1 and date2 and emp_id:
        if request.user.is_authenticated:
            employee = Employee.objects.all()
            if employee:
                for el in employee:
                    if el.USERNAME_FIELD == request.user.username:
                        cr1 = emp_id
                        cr2 = f"'{date1}'"
                        cr3 = f"'{date2}'"
                        cr4 = "'C:/Important/Studing1.3/DB/Practice2-5/report.csv'"
                        # criteries = ((cr1,), (cr2,), (cr3,), (cr4,))
                        with connection.cursor() as cursor:
                            cursor.execute(f"CALL export_to_csv({cr1},{cr2},{cr3},{cr4})")
    if manager == True:
        return render(request, "hello/report.html", {'date1': date1, 'date2': date2, })
    else:
        return render(request, "hello/permission.html")

    
def download_file(request, filename=''):
    file = 'C:/Important/Studing1.3/DB/Practice2-5/report.csv'
    filename = os.path.basename(file)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(file, 'rb'), chunk_size),
                        content_type=mimetypes.guess_type(file)[0])
    response['Content-Length'] = os.path.getsize(file)    
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def income(request):
    income = Income.objects.order_by('income_id')
    users_in_group = Group.objects.get(name="Logistics").user_set.all()
    if request.user in users_in_group:
        return render(request, "hello/income.html", {'income': income})
    else:
        return render(request,"hello/permission.html")

def income_product(request):
    income_id = request.GET.get("income_id")
    income_product = IncomeProduct.objects.filter(income_id = income_id)

    return render(request, "hello/income_product.html", {'income_product': income_product})

def logout_user(request):
    logout(request)
    return redirect('/')

def login_redirect(request):
    return redirect('/')

def product(request):
    search_query = request.GET.get('search', '')
    if search_query:
        product = Product.objects.filter(product_name__contains=search_query)
    else:
        product = Product.objects.all()
    return render(request, "hello/product.html", {'product': product})

def employees(request):
    search_query = request.GET.get('search', '')
    if search_query:
        employee = Employee.objects.filter(emp_name__contains=search_query)
    else:
        employee = Employee.objects.all()
    return render(request,"hello/employees.html", {'employee':employee})

def role_classifier(request):
    role = RoleClassifier.objects.all()
    return render(request, "hello/role_classifier.html", {'role': role})

def cars(request):
    cars = Cars.objects.all()
    return render(request, "hello/cars.html", {'cars':cars})