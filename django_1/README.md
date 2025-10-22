# Django 2 - Course README

## Course Overview
This course focuses on advanced Django development, covering model relationships, forms and validation, authentication systems, and admin customization. Students learn to build robust web applications using Django's powerful ORM and built-in features.

## Learning Objectives
- Master Django model relationships and complex queries
- Implement comprehensive form handling with validation
- Build secure authentication and user management systems
- Customize Django admin interface for better user experience
- Understand Django's ORM and database optimization techniques

## Course Rubric Requirements

### 1. Model Relationships & Queries
- At least 2 related models created using Django ORM, with relationships defined through ForeignKey or ManyToManyField
- Demonstrate proper model relationship definitions
- Show complex queries using Django ORM (filter, exclude, annotate, select_related, prefetch_related)
- Include evidence of relationship traversal and related object access
- Document the model structure and relationship types used

### 2. Django Forms & Validation
- At least 1 Django form created with input validation, using Django's forms.py
- Include custom validation logic or error messages
- Demonstrate form creation using Django's Form or ModelForm classes
- Show custom validation methods and error handling
- Include proper form rendering in templates
- Document form validation rules and error messages

### 3. Authentication & User Management
- At least 1 user authentication system implemented using Django's built-in authentication framework
- Include user registration, login, and logout functionality
- Demonstrate user registration with form validation
- Show login/logout functionality with proper session management
- Include user profile management or user-specific data access
- Document authentication flow and user management features

## Application to HIPAA Checklist Project

### Model Architecture
- **User Model**: Extended Django's built-in User model for healthcare compliance users
- **RegulationUpdate Model**: HIPAA regulations and compliance requirements
- **ChecklistItem Model**: Individual compliance tracking items with risk assessment
- **AuditLog Model**: Complete audit trail for compliance tracking

### Model Relationships
- **Foreign Key Relationships**: ChecklistItem → User, ChecklistItem → RegulationUpdate
- **Many-to-Many**: User roles and permissions for different compliance levels
- **One-to-One**: User profiles with additional healthcare-specific information

### Form Implementation
- **ChecklistItemForm**: ModelForm for creating and updating compliance items
- **UserRegistrationForm**: Custom form for user registration with validation
- **ComplianceReportForm**: Form for generating compliance reports
- **Custom Validation**: HIPAA-specific validation rules and error messages

### Authentication System
- **User Registration**: Secure user registration with email verification
- **Login/Logout**: Session-based authentication with proper security
- **User Profiles**: Extended user profiles with healthcare compliance roles
- **Permission System**: Role-based access control for different compliance levels

## Key Skills Demonstrated
- Django ORM and model relationships
- Complex database queries and optimization
- Form handling and validation
- User authentication and authorization
- Admin interface customization
- Database design and normalization

## Evidence of Completion
- Complete Django models with proper relationships
- Functional forms with custom validation
- Secure authentication system
- Custom admin interface
- Comprehensive testing suite
- Database migrations and schema management

## Technical Stack
- **Framework**: Django 4.2+
- **Database**: SQLite with Django ORM
- **Authentication**: Django's built-in auth system
- **Forms**: Django Forms and ModelForms
- **Admin**: Customized Django admin interface
- **Testing**: Django TestCase and pytest

## Database Schema Highlights
```python
# Key Model Relationships
class ChecklistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    regulation_update = models.ForeignKey(RegulationUpdate, on_delete=models.CASCADE)
    # Additional fields with proper relationships

class RegulationUpdate(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # HIPAA-specific fields
```

## Advanced Features Implemented
- **Encrypted Fields**: Sensitive data encryption using Fernet
- **Audit Logging**: Complete change tracking for compliance
- **Database Indexes**: Performance optimization for queries
- **Custom Managers**: Specialized query methods for compliance data
- **Signal Handlers**: Automated actions on model changes

## Learning Outcomes
Upon completion of this course, students will be able to:
- Design and implement complex Django models with relationships
- Create and validate forms using Django's form system
- Implement secure authentication and user management
- Customize Django admin for specific use cases
- Optimize database queries and performance
- Build scalable web applications with Django

## Compliance Integration
The Django implementation specifically addresses HIPAA compliance requirements:
- **Data Encryption**: Sensitive healthcare data encrypted at rest
- **Audit Logging**: Complete audit trail for regulatory compliance
- **Access Control**: Role-based permissions for different compliance levels
- **Data Integrity**: Proper validation and constraints for healthcare data

---
*This course forms the foundation of the HIPAA Checklist Project's backend architecture, providing secure and compliant data management for healthcare compliance tracking.*
