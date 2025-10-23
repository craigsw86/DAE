# Django 1 - Course README

## Course Overview
This course introduces students to fundamental Django web development, covering project initialization, model definition, view creation, URL mapping, template rendering, static data display, and form processing. Students learn to build dynamic web applications using Django's powerful framework and follow Django's best practices for web development.

## Learning Objectives
- Master Django project initialization and structure
- Learn to define models and database relationships
- Create views and handle HTTP requests
- Implement URL routing and mapping
- Develop HTML templates with Django templating language
- Process forms and handle user input
- Build complete Django web applications

## Course Rubric Requirements

### 1. Project Initialization
- The project can be executed with the 'django-admin startproject' command to create your project structure
- Demonstrate proper Django project setup and configuration
- Show evidence of Django project structure and organization
- Document project initialization and configuration
- Provide examples of Django project best practices
- Show evidence of functional Django project setup

### 2. Model Definition
- At least one model in models.py file including fields relevant to your project's theme and accessible through the Django admin by registering it
- Demonstrate proper model definition and field types
- Show evidence of model registration in Django admin
- Document model structure and relationships
- Provide examples of model usage and functionality
- Show evidence of database integration and admin interface

### 3. View Creation
- At least one view function in views.py that does something (like showing a message) and returns an HTTP response or renders a template
- Demonstrate proper view function implementation
- Show evidence of HTTP response handling
- Document view logic and functionality
- Provide examples of different view types
- Show evidence of template rendering and response handling

### 4. URL Mapping
- At least one URL pattern in your urls.py file that corresponds to your view function
- Demonstrate proper URL pattern configuration
- Show evidence of URL routing and mapping
- Document URL structure and organization
- Provide examples of URL pattern best practices
- Show evidence of functional URL routing

### 5. Template Rendering
- At least one HTML template file that uses Django's templating language (e.g., to display a variable, use {{ variable_name }})
- The template should display content that you pass to it from your view through the context dictionary
- Demonstrate proper Django templating language usage
- Show evidence of template rendering and variable display
- Document template structure and organization
- Provide examples of template inheritance and blocks
- Show evidence of dynamic content rendering

### 6. Static Data Display
- Static data present (like a welcome message or a list of items etc.) that doesn't change
- This should be hard-coded in your template and not come from the database
- Demonstrate static content implementation
- Show evidence of hard-coded template content
- Document static content organization
- Provide examples of static content best practices
- Show evidence of static content display

### 7. Form Processing
- At least one Django form either directly in a view or as a separate form class in forms.py
- This form should be displayed on a template, and once submitted, should show the inputted data on a webpage
- Demonstrate proper Django form implementation
- Show evidence of form display and submission
- Document form processing and validation
- Provide examples of form handling and data processing
- Show evidence of user input processing and display

## Application to HIPAA Checklist Project

### Healthcare Django Project
- **Project Structure**: Django project for healthcare compliance management
- **Healthcare Models**: Patient data, compliance records, audit logs
- **Healthcare Views**: Compliance checking, patient data management
- **Healthcare URLs**: Healthcare-specific URL routing and navigation
- **Healthcare Templates**: HIPAA compliance dashboard and forms
- **Healthcare Forms**: Patient data entry and compliance reporting

### Healthcare Model Definition
- **Patient Model**: Healthcare patient information and medical records
- **Compliance Model**: HIPAA compliance tracking and monitoring
- **Audit Model**: Healthcare audit logs and compliance history
- **User Model**: Healthcare user authentication and authorization
- **Risk Model**: Healthcare risk assessment and management

### Healthcare View Creation
- **Compliance Dashboard**: Healthcare compliance status and monitoring
- **Patient Management**: Patient data viewing and management
- **Risk Assessment**: Healthcare risk evaluation and reporting
- **Audit Logging**: Healthcare compliance audit and logging
- **User Authentication**: Healthcare user login and access control

### Healthcare URL Mapping
- **Compliance URLs**: Healthcare compliance management URLs
- **Patient URLs**: Patient data access and management URLs
- **Risk URLs**: Healthcare risk assessment and reporting URLs
- **Audit URLs**: Healthcare audit and logging URLs
- **Admin URLs**: Healthcare administrative interface URLs

### Healthcare Template Rendering
- **Compliance Dashboard**: Healthcare compliance status display
- **Patient Dashboard**: Patient information and medical records
- **Risk Dashboard**: Healthcare risk assessment and monitoring
- **Audit Dashboard**: Healthcare compliance audit and history
- **Admin Dashboard**: Healthcare administrative interface

### Healthcare Static Data
- **Welcome Messages**: Healthcare application welcome and instructions
- **Compliance Information**: HIPAA compliance guidelines and information
- **Risk Information**: Healthcare risk assessment guidelines
- **Audit Information**: Healthcare audit procedures and requirements
- **User Information**: Healthcare user roles and permissions

### Healthcare Form Processing
- **Patient Data Forms**: Patient information entry and management
- **Compliance Forms**: HIPAA compliance reporting and tracking
- **Risk Assessment Forms**: Healthcare risk evaluation and reporting
- **Audit Forms**: Healthcare compliance audit and logging
- **User Management Forms**: Healthcare user registration and management

## Key Skills Demonstrated
- Django project initialization and configuration
- Model definition and database integration
- View creation and HTTP request handling
- URL mapping and routing
- Template rendering and dynamic content
- Static content implementation
- Form processing and user input handling

## Evidence of Completion
- Functional Django project created with 'django-admin startproject'
- At least one model defined in models.py with admin registration
- At least one view function in views.py with HTTP response
- At least one URL pattern in urls.py corresponding to view
- At least one HTML template with Django templating language
- Static data displayed in template
- At least one Django form with display and submission functionality

## Technical Stack
- **Framework**: Django 4.2+
- **Database**: SQLite, PostgreSQL, MySQL
- **Templates**: Django templating language, HTML5
- **Forms**: Django Forms, ModelForms
- **Admin**: Django admin interface
- **Static Files**: CSS, JavaScript, images

## Healthcare Django Project Structure
```python
# Django Project Structure
hipaa_checklist_project/
├── manage.py
├── hipaa_checklist_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── compliance/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── compliance/
└── static/
    ├── css/
    ├── js/
    └── images/
```

## Healthcare Model Definition
```python
# compliance/models.py
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    """Healthcare patient model for HIPAA compliance."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    medical_record_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ComplianceRecord(models.Model):
    """HIPAA compliance tracking model."""
    RISK_LEVELS = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
        ('CRITICAL', 'Critical Risk'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    compliance_type = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS)
    is_compliant = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient} - {self.compliance_type}"

class AuditLog(models.Model):
    """Healthcare audit logging model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
```

## Healthcare View Creation
```python
# compliance/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Patient, ComplianceRecord, AuditLog
from .forms import PatientForm, ComplianceForm

def home(request):
    """Healthcare application home page."""
    context = {
        'welcome_message': 'Welcome to HIPAA Compliance Management System',
        'total_patients': Patient.objects.count(),
        'total_compliance_records': ComplianceRecord.objects.count(),
    }
    return render(request, 'compliance/home.html', context)

@login_required
def patient_list(request):
    """Display list of healthcare patients."""
    patients = Patient.objects.all()
    context = {
        'patients': patients,
        'page_title': 'Patient Management'
    }
    return render(request, 'compliance/patient_list.html', context)

@login_required
def compliance_dashboard(request):
    """Healthcare compliance dashboard."""
    compliance_records = ComplianceRecord.objects.all()
    high_risk_records = compliance_records.filter(risk_level='HIGH')
    
    context = {
        'compliance_records': compliance_records,
        'high_risk_records': high_risk_records,
        'page_title': 'Compliance Dashboard'
    }
    return render(request, 'compliance/dashboard.html', context)

def add_patient(request):
    """Add new healthcare patient."""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='Patient Added',
                patient=patient,
                details=f'Added patient: {patient.first_name} {patient.last_name}'
            )
            return redirect('patient_list')
    else:
        form = PatientForm()
    
    context = {
        'form': form,
        'page_title': 'Add New Patient'
    }
    return render(request, 'compliance/add_patient.html', context)
```

## Healthcare URL Mapping
```python
# compliance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patients/', views.patient_list, name='patient_list'),
    path('dashboard/', views.compliance_dashboard, name='dashboard'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('compliance/', views.compliance_dashboard, name='compliance'),
]

# hipaa_checklist_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('compliance.urls')),
]
```

## Healthcare Template Rendering
```html
<!-- compliance/templates/compliance/home.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HIPAA Compliance Management</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background-color: #2c3e50; color: white; padding: 20px; }
        .content { margin: 20px 0; }
        .stats { display: flex; gap: 20px; }
        .stat-box { background-color: #ecf0f1; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ welcome_message }}</h1>
    </div>
    
    <div class="content">
        <h2>System Overview</h2>
        <div class="stats">
            <div class="stat-box">
                <h3>Total Patients</h3>
                <p>{{ total_patients }}</p>
            </div>
            <div class="stat-box">
                <h3>Compliance Records</h3>
                <p>{{ total_compliance_records }}</p>
            </div>
        </div>
        
        <h2>Quick Actions</h2>
        <ul>
            <li><a href="{% url 'patient_list' %}">View Patients</a></li>
            <li><a href="{% url 'dashboard' %}">Compliance Dashboard</a></li>
            <li><a href="{% url 'add_patient' %}">Add New Patient</a></li>
        </ul>
    </div>
</body>
</html>
```

## Healthcare Form Processing
```python
# compliance/forms.py
from django import forms
from .models import Patient, ComplianceRecord

class PatientForm(forms.ModelForm):
    """Healthcare patient form."""
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'medical_record_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_medical_record_number(self):
        """Validate medical record number."""
        medical_record_number = self.cleaned_data.get('medical_record_number')
        if Patient.objects.filter(medical_record_number=medical_record_number).exists():
            raise forms.ValidationError('Medical record number already exists.')
        return medical_record_number

class ComplianceForm(forms.ModelForm):
    """HIPAA compliance form."""
    class Meta:
        model = ComplianceRecord
        fields = ['patient', 'compliance_type', 'risk_level', 'is_compliant', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
```

## Healthcare Admin Configuration
```python
# compliance/admin.py
from django.contrib import admin
from .models import Patient, ComplianceRecord, AuditLog

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'medical_record_number', 'created_at']
    list_filter = ['created_at']
    search_fields = ['first_name', 'last_name', 'medical_record_number']

@admin.register(ComplianceRecord)
class ComplianceRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'compliance_type', 'risk_level', 'is_compliant', 'created_at']
    list_filter = ['risk_level', 'is_compliant', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'compliance_type']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'patient', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__username', 'action', 'patient__first_name']
```

## Learning Outcomes
Upon completion of this course, students will be able to:
- Initialize Django projects and configure settings
- Define models and database relationships
- Create views and handle HTTP requests
- Implement URL routing and mapping
- Develop HTML templates with Django templating language
- Process forms and handle user input
- Build complete Django web applications

## Healthcare Compliance Integration
The Django implementation specifically addresses healthcare compliance needs:
- **HIPAA Compliance**: All Django features aligned with HIPAA requirements
- **Patient Data Protection**: Secure handling of Protected Health Information
- **Audit Logging**: Comprehensive audit trails for compliance
- **User Management**: Healthcare user authentication and authorization
- **Data Validation**: Healthcare data validation and security

## Advanced Django Concepts
- **Model Relationships**: Foreign keys and many-to-many relationships
- **Template Inheritance**: Base templates and template blocks
- **Form Validation**: Custom validation and error handling
- **Admin Customization**: Custom admin interface and functionality
- **Security**: Django security features and best practices

---
*This course provides the Django foundation for the HIPAA Checklist Project, ensuring secure and compliant web development for healthcare applications.*
