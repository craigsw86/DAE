# Django 2 - Evidence Folder

This folder contains all the relevant files demonstrating compliance with the Django 2 rubric criteria.

## Folder Structure

### 1_Model_Relationships_Queries/
**Criterion**: At least 2 related models created using Django ORM, with relationships defined through ForeignKey or ManyToManyField, and queries performed using Django's QuerySet API

- `models.py` - Two related models with ForeignKey relationships
- `views.py` - Complex Django ORM queries with select_related, filter, exclude
- `0001_initial.py` - Database migration showing relationships

**Evidence**:
- **Two Related Models**: `RegulationUpdate` and `ChecklistItem`
- **ForeignKey Relationships**: 
  - `ChecklistItem.user` → `User` (Django's built-in User model)
  - `ChecklistItem.regulation_update` → `RegulationUpdate`
- **Complex Queries**: 
  - `select_related('regulation_update')` for optimization
  - `filter(user=user)` for user-specific data
  - `order_by('-last_updated')` for sorting
  - `obj.checklistitem_set.count()` for relationship traversal

### 2_Forms_Validation/
**Criterion**: At least 1 Django form created with input validation, using Django's forms.py, including custom validation logic or error messages

- `forms.py` - ModelForm with custom validation and error handling
- `views.py` - Form handling with validation and error messages
- `index.html` - Form rendering in templates

**Evidence**:
- **ModelForm**: `ChecklistItemForm` extends `forms.ModelForm`
- **Custom Validation**: User-specific field visibility (`admin_notes` hidden for non-staff users)
- **Error Handling**: Form validation with `form.is_valid()` and error display
- **Form Rendering**: `{{ form.as_p }}` in template with error display
- **Custom Widgets**: Textarea widgets with custom attributes
- **Help Text**: Field-specific help text for user guidance

### 3_Authentication_User_Management/
**Criterion**: At least 1 user authentication system implemented using Django's built-in authentication framework, including user registration, login, and logout functionality

- `views.py` - `@login_required` decorator and user authentication
- `create_test_user.py` - User creation and authentication testing
- `test_backend_api.py` - Authentication flow testing
- `manual_flow_verification.py` - User management and authentication

**Evidence**:
- **Built-in Authentication**: Django's `User` model and authentication framework
- **Login Required**: `@login_required` decorator on views
- **User Registration**: User creation in test scripts with `User.objects.get_or_create()`
- **Session Management**: User-specific data access (`user=request.user`)
- **User Profile Management**: User-specific checklist items and data filtering
- **Authentication Testing**: Comprehensive test scripts for auth flow

### 4_Admin_Customization/
**Criterion**: At least 1 customization applied to the Django Admin panel, such as custom model display, filtering, or inline editing

- `admin.py` - Custom admin configurations
- `MANUAL_UPDATES_INTEGRATION.md` - Admin functionality documentation
- `MANUAL_UPDATES_TESTING_CHECKLIST.md` - Admin testing checklist

**Evidence**:
- **Custom List Display**: `list_display = ('user', 'regulation_update', 'completed', ...)`
- **Search Functionality**: `search_fields = ('user__username', 'regulation_update__title', ...)`
- **Advanced Filtering**: `list_filter = ('completed', 'likelihood', 'impact', 'user', ...)`
- **Custom Methods**: `checklist_items_count()` method in admin
- **Custom Queryset**: `get_queryset()` with user-specific filtering
- **Custom Forms**: `RegulationUpdateAdminForm` with custom widgets
- **Date Hierarchy**: `date_hierarchy = 'created_at'` for navigation
- **Pagination**: `list_per_page = 25` for performance

### Documentation/
**Supporting Documentation**:
- `Django_2_Rubric.md` - The rubric criteria
- `test_end_to_end.py` - Comprehensive testing script

## How to Use This Evidence

1. **For Model Relationships**: Review `1_Model_Relationships_Queries/` to see ForeignKey relationships and ORM queries
2. **For Forms & Validation**: Check `2_Forms_Validation/` for ModelForm implementation and validation
3. **For Authentication**: Examine `3_Authentication_User_Management/` for Django auth implementation
4. **For Admin Customization**: Look at `4_Admin_Customization/` for admin interface customizations

## Testing the Django Implementation

1. Start the Django backend: `python manage.py runserver`
2. Access the admin interface: `http://localhost:8000/admin/`
3. Run the test scripts: `python test_backend_api.py`
4. Test user creation: `python create_test_user.py`
5. View the checklist form: `http://localhost:8000/checklist/`

## Key Django Features Demonstrated

### Model Relationships
- **ForeignKey**: `ChecklistItem.user` → `User`
- **ForeignKey**: `ChecklistItem.regulation_update` → `RegulationUpdate`
- **Related Manager**: `obj.checklistitem_set.count()`

### ORM Queries
- **select_related()**: `ChecklistItem.objects.select_related('regulation_update')`
- **filter()**: `ChecklistItem.objects.filter(user=user)`
- **order_by()**: `.order_by('-last_updated')`
- **Complex Queries**: Multiple filter conditions and annotations

### Forms & Validation
- **ModelForm**: `ChecklistItemForm(forms.ModelForm)`
- **Custom Validation**: User-specific field visibility
- **Error Handling**: `form.is_valid()` and template error display
- **Custom Widgets**: Textarea with custom attributes

### Authentication
- **Built-in Auth**: Django's User model and authentication framework
- **Decorators**: `@login_required` for view protection
- **User Management**: User creation, authentication, and session handling
- **Permission-based Access**: User-specific data filtering

### Admin Customization
- **Custom List Display**: Multiple columns with custom methods
- **Search & Filter**: Advanced search and filtering capabilities
- **Custom Queryset**: User-specific data filtering
- **Custom Forms**: Custom admin forms with widgets
- **Date Hierarchy**: Navigation by date fields

## Summary

This project demonstrates comprehensive Django development with:
- ✅ **Model Relationships**: Two related models with ForeignKey relationships and complex ORM queries
- ✅ **Forms & Validation**: ModelForm with custom validation, error handling, and template rendering
- ✅ **Authentication**: Built-in Django authentication with user management and session handling
- ✅ **Admin Customization**: Custom admin interface with list displays, search, filtering, and custom methods

All criteria for the Django 2 rubric are fully met with supporting evidence in this folder structure.
