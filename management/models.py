from django.db import models

class Admin(models.Model):
    username = models.CharField(verbose_name="Username", max_length=32)
    password = models.CharField(verbose_name="Password", max_length=64)

class Department(models.Model):
    name = models.CharField(max_length=32)
    location = models.CharField(max_length=32)
    
    # Make department input box return the actual department names rather than object memory address
    def __str__(self):
        return self.name
    
class Staff(models.Model):
    name = models.CharField(verbose_name="Name", max_length=16)
    age = models.IntegerField(verbose_name="Age")
    # Django Constraints: 'gender' can only be 1, 2, 3/4
    gender_choices = (
        (1, "Male"),
        (2, "Female"),
        (3, "Transgender"),
        (4, "Gender Neutral")
    )
    
    # Database will store gender as numbers (1, 2, 3/4), UI will display texts
    gender = models.SmallIntegerField(choices=gender_choices, default=None)
    salary = models.DecimalField(verbose_name="Salary", max_digits=10, decimal_places=2)
    joining_date = models.DateField(verbose_name="Joining Date")
    
    
    
    # Connect table 'department' to 'staff'
    # We will use department id rather than department name
    # 'department_id' must be limited, it's value can only be existing id in table 'department'
    # When 'department_id' IS NOT constrained/restricted
    # department_id = models.BigIntegerField()
    
    # When 'department_id' IS constrained/restricted
    # Note:
    # Django ORM will automatically add '_id' to 'department',
    # therefore, in MySQL database, table 'Staff' column will be 'department_id' 
    
    # on_delete=models.CASCADE
    # Sets the behavior when the referenced Department instance is deleted. models.CASCADE means that if the related Department object is deleted, any object with this foreign key reference will also be deleted (cascading the delete).
    
    department = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    
    
    is_registered_choices = [
        (True, "Registered"),
        (False, "Unregistered"),
    ]
    is_registered = models.BooleanField(verbose_name="Registration Status", choices= is_registered_choices, default=None)
    
    def __str__(self):
        return self.name
    
class Task(models.Model):
    title = models.CharField(verbose_name="Title", max_length=255)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    assigned_department = models.ForeignKey(verbose_name="Assigned Department", to="Department", to_field="id", on_delete=models.CASCADE, null=True, blank=True)
    assigned_staff = models.ForeignKey(verbose_name="Assigned Staff", to="Staff", to_field="id", on_delete=models.CASCADE, null=True, blank=True)
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent')
    ]
    
    priority = models.CharField(verbose_name="Priority", max_length=10, choices=PRIORITY_CHOICES, default=None)
    
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
        ('Canceled', 'Canceled')
    ]
    
    status = models.CharField(verbose_name="Status", max_length=20, choices=STATUS_CHOICES, default=None)
    
    
# Define the through model with extra fields
class TaskAssignment(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assigned_date = models.DateField(verbose_name="Assigned Date")
    completion_deadline = models.DateField(verbose_name="Completion Deadline")

    def __str__(self):
        return f"{self.staff.name} - {self.task.title} assigned on {self.assigned_date}"
    
    
    
class Order(models.Model):
    order_id = models.CharField(verbose_name="Order ID", max_length=64)
    price = models.IntegerField(verbose_name="Total Amount (£)")
    
    is_paid_choices = [
        (True, "Paid"),
        (False, "Unpaid"),
    ]
    is_paid = models.BooleanField(verbose_name="Payment Status", choices= is_paid_choices, default=None)
    
    status_choices = [
        (1, "Pending"),
        (2, "Shipped"),
        (3, "Delivered"),
        (4, "Canceled"),
        (5, "Returned"),
    ]
    status = models.SmallIntegerField(verbose_name="Order Status", choices=status_choices, default=None)
    
    responsible_staff = models.ForeignKey(verbose_name="Responsible Staff Member", to="Staff", on_delete=models.CASCADE)
    
    
    
    
    
    
    