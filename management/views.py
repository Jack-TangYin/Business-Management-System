from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from management import models
from management.utils.pagination import Pagination
from management.utils.encryption import md5
from management.utils.random_image_generator import check_code
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
import json 
from django.http import JsonResponse
from django.http import QueryDict


def index(request):
    return render(request, "index.html")



def department_list(request):
    # 1. Get all department info from table 'management_department' from database 'django_tutorial'
    # 'models.Department.objects.all()' has a type of queryset, a list contains objects
    queryset = models.Department.objects.all()
    page_obj = Pagination(request, queryset, page_size=3)
    context = {
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html(),
    }
    
    return render(request, "department_list.html", context)

def department_create(request):
    if request.method == "GET":
        return render(request, "department_create.html")
    elif request.method == "POST":
        # Get user submitted data via POST
        name = request.POST.get("name")
        location = request.POST.get("location")
        
        # Save user submitted data to database
        models.Department.objects.create(name = name, location = location)
        
        # Redirect to Department Management (list)
        return redirect("/department/list/")

def department_delete(request):
    # Get ID for the data that need to be deleted
    # E.g. 'http://127.0.0.1:8000/department/delete/?nid=1'
    # In this case 'request.GET.get('nid')' will be 1
    nid = request.GET.get('nid')
    # Delete the data that has the specified ID
    models.Department.objects.filter(id=nid).delete()
    
    # Redirect back to the department management list
    return redirect("/department/list/")

# The parameter 'nid' represents the real value of nid passed via the URL.
# E.g. If URL = 'http://127.0.0.1:8000/department/10/edit/'
# Then parameter 'nid' = 10
def department_edit(request, nid):
    if request.method == "GET":
    # Get matching data via 'nid' when clicking on the edit button for a department
    # Because 'models.Department.objects.filter(id = nid)' returns a queryset that consists of many objects,
    # Using 'first()' will get the first object and it's related data
        row_object = models.Department.objects.filter(id = nid).first()
    
        print(row_object.id, row_object.name, row_object.location)
        return render(request, "department_edit.html", {"row_object": row_object})
    elif request.method == "POST":
        # Get the user edited department name
        name = request.POST.get("name")
        # Get the user edited department location
        location = request.POST.get("location")
        
        # Find the data that has an id of 'nid' and update it with user submitted data
        models.Department.objects.filter(id = nid).update(name = name, location = location)
        
        # Redirect to department list
        return redirect("/department/list/")
        
        
        
def staff_list(request):
    # Get All Fields with Their Verbose Names via a loop
    fields = [field.verbose_name for field in models.Staff._meta.fields]
    
    # 1. Get all staff data from the database
    queryset = models.Staff.objects.all()
    
    page_obj = Pagination(request, queryset, page_size=3)
    context = {
        "fields": fields,
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html(),
    }
    """ The following is achieved by Python grammar"""
    # for obj in queryset:
    #     # 'obj.joining_date' has a type of 'datetime', therefore we need to convert it to string via '.strftime' 
    #     # '.strftime("%Y-%m-%d")' ensures the string will only show year-month-day 
        
    #     # 'get_gender_display()' is used with model fields that have choices defined. 
    #     # This method provides the human-readable name (or "display value") for the currently selected choice rather than the raw database value.
    #     # 'obj.gender' will display the raw database value: 1 / 2 / 3 / 4
    #     print(obj.get_gender_display(), obj.joining_date.strftime("%Y-%m-%d"))
        
    #     obj.department_id  # Get the raw data from the database: 1 / 2 / 21 / 22
        
    #     # 'obj.department' will get you the data object that has the matching id in the 'management_department' table
    #     # In conclusion, 'obj.department' will help you do achieve cross-table actions
    #     obj.department.name  # Because 'obj.department' is an object representing the matching data in the 'management_department' table, you can do 'obj.department.name' to get the specific data you want
        
    
    # To achieve the same outcome as above in Django, the grammar is different, see how it is done in "staff_list.html"
    return render(request, "staff_list.html", context)


# def staff_create(request):
    if request.method == "GET":
        # Get all genders and department names from the database
        info_dict = {
            "gender_choices": models.Staff.gender_choices,
            "department_list": models.Department.objects.all()
        }
        return render(request, "staff_create.html", info_dict)      
    elif request.method == "POST":
        # 1. Get all user submitted date via post
        # variable name = request.POST.get("name value in html <input> / <select>")
        name = request.POST.get("name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        salary = request.POST.get("salary")
        joining_date = request.POST.get("joining_date")
        department_id = request.POST.get("department")
        
        # 2. Add user submitted date to the database 
        models.Staff.objects.create(
            name = name, 
            age = age, 
            gender = gender, 
            salary = salary, 
            joining_date =joining_date, 
            department_id = department_id
        )
        
        # 3. Redirect back to the webpage that shows staff list
        return redirect("/staff/list/")   

""" ------------------------------- ModelForm Demo ------------------------------- """
# Module 'forms' provides tools to create and manage forms in Django applications.
from django import forms
# Create a new class called StaffModelForm that inherits from forms.ModelForm. 
# This means that your form will automatically include functionality for working with a Django model.
class StaffModelForm(forms.ModelForm):
    # joining_date = forms.DateField(disabled=True, label="Joining Date")
    # The Meta class inside StaffModelForm provides configuration options for the form. It contains:
    class Meta:
        # This specifies which Django model the form is associated with. 
        # In this case, it’s 'models.Staff'. 
        # You need to ensure you import the models module where Staff is defined.
        model = models.Staff
        # Django automatically handles the creation of input fields for name, age, and salary based on their definitions in the Staff model.
        fields = "__all__"
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),  
        # }
        widgets = {
            'joining_date': forms.DateInput(format='%d-%m-%Y'),
        }
        
    joining_date = forms.DateField(
        input_formats=['%d-%m-%Y']
    )
        
    def __init__(self, *args, **kwargs):
        # Redefine __init__ Method
        super().__init__(*args, **kwargs)
        
        # Add a default option "--Please choose an option--" to select fields with choices
        if 'department' in self.fields:
            self.fields['department'].empty_label = "--Please choose an option--"
        
        # Custom default option for the gender field
        if 'gender' in self.fields:
            self.fields['gender'].choices = [("", "--Please choose an option--")] + list(self.fields['gender'].choices)
        
        if 'is_registered' in self.fields:
            self.fields['is_registered'].choices = [("", "--Please choose an option--")] + list(self.fields['is_registered'].choices)
            
        # Change the label of the salary field to include the currency symbol
        self.fields['salary'].label = "Salary (£)"
        
        self.fields['joining_date'].label = "Joining Date"
            
        # Find all widgets via loop and add style "class": "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

def staff_create_modelform(request): 
    if request.method == "GET":
        form = StaffModelForm()
        return render(request, "staff_create_modelform.html", {"form": form})
    elif request.method == "POST":
        # Creating an instance of StaffModelForm with data from the form submission (i.e., the data the user entered in the form). 
        form = StaffModelForm(data = request.POST)
        if form.is_valid():
            # If user entered the correct info
            # Then we can get every data like the following:
            # {'name': '1', 'age': 1, 'gender': 1, 'salary': Decimal('121212'), 'joining_date': datetime.datetime(2000, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'department': <Department: Customer Service>}
            # print(form.cleaned_data)
            # We then need to save the data to the database
            form.save()
            return redirect("/staff/list/")
            
        else:
            return render(request, "staff_create_modelform.html", {"form": form})

 
class StaffEditModelForm(forms.ModelForm):
    joining_date = forms.DateField(disabled=True, label="Joining Date")
    # The Meta class inside StaffModelForm provides configuration options for the form. It contains:
    class Meta:
        # This specifies which Django model the form is associated with. 
        # In this case, it’s 'models.Staff'. 
        # You need to ensure you import the models module where Staff is defined.
        model = models.Staff
        # Django automatically handles the creation of input fields for name, age, and salary based on their definitions in the Staff model.
        fields = "__all__"
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),  
        # }
        widgets = {
            'joining_date': forms.DateInput(format='%d-%m-%Y'),
        }
        
    def __init__(self, *args, **kwargs):
        # Redefine __init__ Method
        super().__init__(*args, **kwargs)
         
        # Find all widgets via loop and add style "class": "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
            
def staff_edit(request, id):
    # Get the data of the row that needs to be edited according to row id
    row_object = models.Staff.objects.filter(id = id).first()
    
    if request.method == "GET":
        # 'instance = row_object' will make Django display all data of the matching id row on input boxes by default
        form = StaffEditModelForm(instance = row_object)

        return render(request, "staff_edit.html", {"form":form})           
    elif request.method == "POST":
        # Get user edited data
        form = StaffEditModelForm(data = request.POST, instance = row_object)
        # Check the validity of user edited data 
        if form.is_valid():
            # Store user edited data to the database if validation is passed
            form.save()
            return redirect("/staff/list/")
        else:
            return render(request, "staff_edit.html", {"form":form})

def staff_delete(request, id):
    models.Staff.objects.filter(id = id).delete()    
    return redirect('/staff/list/')



def task_list(request):
    # Get All Fields with Their Verbose Names via a loop
    fields = [field.verbose_name for field in models.Task._meta.fields]
    
    # for i in range(100):
    #     models.Task.objects.create(title="Training Session", description="Organize training for new employees.", assigned_department_id=21, assigned_staff_id=7, priority="High", status="In Progress")
    
    data_dict = {}
    
    # If user did not pass any q value, then search_data = ""
    search_data = request.GET.get('q', "")
    
    if search_data:  # If users submit the form via the input that has a name of 'q'
        data_dict["title__icontains"] = search_data  # Use icontains for case-insensitive match
    
    queryset = models.Task.objects.filter(**data_dict)
    page_obj = Pagination(request, queryset)
    
    page_queryset = page_obj.page_queryset
     
    page_string = page_obj.html()
    
    context = {
        "fields": fields, 
        "search_data":search_data, 
        "queryset": page_queryset, 
        "page_string":page_string,
    }
        
    
    return render(request, "task_list.html", context)

class TaskModelForm(forms.ModelForm): 
    class Meta:
        model = models.Task
        
        # All fields
        fields = "__all__"
        # Customized Fields
        # fields = ["title", "description", "assigned_department", "assigned_staff", "priority", "status"]
        # # All fields but "status"
        # exclude = ["status"]
        
    def __init__(self, *args, **kwargs):
        # Redefine __init__ Method
        super().__init__(*args, **kwargs)
        
        # Custom default option for the priority field
        if 'priority' in self.fields:
            self.fields['priority'].choices = [("", "--Please choose an option--")] + list(self.fields['priority'].choices)
       
        # Custom default option for the status field
        if 'status' in self.fields:
            self.fields['status'].choices = [("", "--Please choose an option--")] + list(self.fields['status'].choices)
        
        # Add a default option "--Please choose an option--" to select fields with choices
        if 'assigned_department' in self.fields:
            self.fields['assigned_department'].empty_label = "--Please choose an option--"
            
        if 'assigned_staff' in self.fields:
            self.fields['assigned_staff'].empty_label = "--Please choose an option--"
            
        
        # Find all widgets via loop and add style "class": "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
    
    # Check if title exists already and raise error if it does
    def clean_title(self):
        title = self.cleaned_data["title"]
        # Check for other duplications excluding the data that is being edited
        title_exists = models.Task.objects.exclude(id=self.instance.pk).filter(title=title).exists()
        if title_exists:
            raise forms.ValidationError("This title already exists!")
        else:  
            return title

def task_create(request):
    if request.method == "GET":
        form = TaskModelForm()
        return render(request, "task_create.html", {"form": form})
    elif request.method == "POST":
        # Creating an instance of StaffModelForm with data from the form submission (i.e., the data the user entered in the form). 
        form = TaskModelForm(data = request.POST)
        if form.is_valid():
            # If user entered the correct info
            # Then we can get every data like the following:
            # {'name': '1', 'age': 1, 'gender': 1, 'salary': Decimal('121212'), 'joining_date': datetime.datetime(2000, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'department': <Department: Customer Service>}
            # print(form.cleaned_data)
            # We then need to save the data to the database
            form.save()
            return redirect("/task/list/")
            
        else:
            return render(request, "task_create.html", {"form": form})

def task_edit(request, id):
    # Get the data of the row that needs to be edited according to row id
    row_obj = models.Task.objects.filter(id = id).first()
    
    if request.method == "GET":
        # 'instance = row_object' will make Django display all data of the matching id row on input boxes by default
        form = TaskModelForm(instance = row_obj)

        return render(request, "task_edit.html", {"form":form})           
    elif request.method == "POST":
        # Get user edited data
        form = TaskModelForm(data = request.POST, instance = row_obj)
        # Check the validity of user edited data 
        if form.is_valid():
            # Store user edited data to the database if validation is passed
            form.save()
            return redirect("/task/list/")
        else:
            return render(request, "task_edit.html", {"form":form})
        
def task_delete(request, id):
    models.Task.objects.filter(id = id).delete()
    return redirect("/task/list/")       
    

def admin_list(request):
    # Get All Fields with Their Verbose Names via a loop
    fields = [field.verbose_name for field in models.Admin._meta.fields]
    
    # Search Bar Function
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__icontains"] = search_data
    
    # Get the data from the database that matches user searching conditions
    # If there is no q value obtained, then data_dict is empty, calling filter(**data_dict) will effectively return all records in the database.
    queryset = models.Admin.objects.filter(**data_dict)
    # Pagination
    page_obj = Pagination(request, queryset)
    
    context = {
        "fields": fields,
        "queryset": queryset,   
        "page_string": page_obj.html(),
        "search_data": search_data
    }
    
    return render(request, "admin_list.html", context)

class AdminModelForm(forms.ModelForm):
    # Confirm Password (custom field)
    # Why is the widget set outside of class Meta?
    # Custom fields need to have their widgets set directly on the field itself, 
    # as the Meta.widgets only applies to fields defined within the model.
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput()
    )
    
    class Meta:
        model = models.Admin
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput(),
        }
    
    def __init__(self, *args, **kwargs):
        # Redefine __init__ Method
        super().__init__(*args, **kwargs)
         
        # Find all widgets via loop and add style "class": "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        
        # If editing, compare new password with the current one
        if self.instance.pk:
            current_password = self.instance.password
            if md5_pwd == current_password:
                raise ValidationError("New password cannot be the same as your current password.")
        return md5_pwd
    
    def clean_confirm_password(self):
        # Skip confirm_password validation if there's already an error on password
        if self.errors.get("password"):
            return self.cleaned_data.get("confirm_password")
        
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        # Compare whether encrypted password and encrypted confirm_password are the same
        if confirm != pwd:
            raise ValidationError("Passwords do not match")
        # Return value does not have a meaning here because custom field 'confirm_password' will NOT be saved in the database.
        # In the future, the return value will be saved in the database if needed
        return confirm
     
def admin_create(request):
    title = "Create New Admin"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "create_edit.html", {"form": form, "title": title})
    elif request.method == "POST":
        form = AdminModelForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect("/admin/list/")
    
        return render(request, "create_edit.html", {"form": form, "title": title})

def admin_edit(request, id):
    # Get current page object
    # If successful (id exists), then an object will be obtained
    # If unsuccessful, then value None will be obtained
    row_obj = models.Admin.objects.filter(id = id).first()
    if not row_obj:
        return render(request, "error.html", {"msg": "No Results Found"})
    
    title = "Edit Existing Admin"    
    
    if request.method == "GET":
        form = AdminModelForm(instance=row_obj)
        return render(request, "create_edit.html", {"form": form, "title": title})   
    elif request.method == "POST":
        form = AdminModelForm(data=request.POST, instance=row_obj)
        if form.is_valid():
            form.save()
            return redirect("/admin/list/")
        else:
            # Display errors
            return render(request, "create_edit.html", {"form": form, "title": title})  
               
def admin_delete(request, id):
    models.Admin.objects.filter(id = id).delete()
    return redirect("/admin/list/")



class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=True)
    )
    captcha = forms.CharField(
        label="CAPTCHA",
        widget=forms.TextInput,
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        # Redefine __init__ Method
        super().__init__(*args, **kwargs)

        # Find all widgets via loop and add style "class": "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
        
        # Set a custom placeholder for the 'captcha' field
        self.fields['captcha'].widget.attrs['placeholder'] = 'Enter the 5-digit code here'
    
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
        

def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            
            # Get User input CAPTCHA code
            # Must use pop() so User input CAPTCHA code will be removed after obtaining it
            # So 'admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()' will work normally
            user_input_code = form.cleaned_data.pop("captcha")
            image_code = request.session.get("image_code", "")
            if image_code.upper() != user_input_code.upper():
                form.add_error("captcha", "Incorrect CAPTCHA code")
                return render(request, "login.html", {"form": form}) 
                
            
            # Check user entered info against the database
            # Get user object
            admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
    
            if not admin_obj:
                form.add_error("password", "Incorrect username or password.")
                return render(request, "login.html", {"form": form}) 
            
            # When Username and Password are correct
            # Website randomly generates a string, place it in browser's cookie (can be checked via the network section in F12)
            # The string will also be placed in column 'session_key' of django pre built-in table 'django_session'
            request.session["user_info"] = {'id': admin_obj.id, "name": admin_obj.username }
            
            # User info will saved in session for 7 days => User no need to login again for another week once they logged in
            request.session.set_expiry(60 * 60 * 24 * 7)
            
            return redirect("/admin/list/")
        
        return render(request, "login.html", {"form": form})

def image_random(request):
    # Call the pillow function, and generate the random image
    img, code_str = check_code()
    
    # Write it in session so it can be obtained and used for authentication
    request.session['image_code'] = code_str
    # Make the image only valid within 60 seconds 
    request.session.set_expiry(60)
    
    stream = BytesIO()
    img.save(stream, "png")
    img_content = stream.getvalue()
    return HttpResponse(img_content)

def logout(request):
    
    request.session.clear()
    
    return redirect("/login/")   

class OrderModelForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Redefine __init__ Method
        super().__init__(*args, **kwargs)
        
        # Custom widget for is_paid field to display True/False as choices
        if 'is_paid' in self.fields:
            self.fields['is_paid'].choices = [("", "--Please choose an option--")] + list(self.fields['is_paid'].choices)
       
        # Custom default option for the status field
        if 'status' in self.fields:
            self.fields['status'].choices = [("", "--Please choose an option--")] + list(self.fields['status'].choices)
        
        # Add a default option "--Please choose an option--" to select fields with choices
        if 'responsible_staff' in self.fields:
            self.fields['responsible_staff'].empty_label = "--Please choose an option--"
            
        # Find all widgets via loop and add style "class": "form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
    
def order_list(request):
    # Get All Fields with Their Verbose Names via a loop
    fields = [field.verbose_name for field in models.Order._meta.fields]
    
    queryset = models.Order.objects.all()
    
    # Pagination
    page_obj = Pagination(request, queryset)
    page_queryset = page_obj.page_queryset
    
    form = OrderModelForm()
    
    context = {
        "fields": fields,
        "queryset": page_queryset,   
        "form": form,
        "page_string": page_obj.html(),
    }
    
    return render(request, "order_list.html", context)

@csrf_exempt
def order_create(request):
    """Handle AJAX POST request to create a new order"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        new_order = form.save()  # Save and get the new order instance

        # Prepare data to return for the new row
        return JsonResponse({
            "status": True,
            "order": {
                "id": new_order.id,
                "order_id": new_order.order_id,
                "price": new_order.price,
                "is_paid": new_order.get_is_paid_display(),
                "status": new_order.get_status_display(),
                "responsible_staff": new_order.responsible_staff.name,
            }
        })
    else:
        # Return form errors if the form is invalid
        return JsonResponse({"status": False, 'error': form.errors})
    
    
@csrf_exempt
def order_delete(request):
    # Check if the request method is DELETE
    if request.method == "DELETE":
         # Read the JSON data from the body of the request
        data = json.loads(request.body)  # Parse the incoming JSON body
        uid = data.get("uid")  # Get the 'uid' (order ID) from the parsed data
        
        # Check if the order with the given 'uid' exists in the database
        exists = models.Order.objects.filter(id=uid).exists()
        if not exists:
            # If the order does not exist, return a failure response
            return JsonResponse({"status": False, "error": "Deletion Failed: Data does not exist."})
        
        # If the order exists, delete it from the database
        models.Order.objects.filter(id=uid).delete()
        
        # Return a success response after deletion
        return JsonResponse({"status": True})
    
     # If the request method is not DELETE, return an error indicating an invalid request method
    else:
        return JsonResponse({"status": False, "error": "Invalid request method."})

def order_info(request):
    # Get order info data according to ID
    
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values().first()
    if not row_dict:  
        return JsonResponse({"status": False, "error": "Deletion Failed: Data does not exist."})
    
    result = {
        "status": True,
        "data": row_dict
    }
        
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """ 编辑订单 """
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在，请刷新重试。"})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})
    
    





    