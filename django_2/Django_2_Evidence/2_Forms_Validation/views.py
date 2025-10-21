from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import RegulationUpdate, ChecklistItem
from .serializers import RegulationUpdateSerializer, ChecklistItemSerializer
from django.contrib.auth.decorators import login_required
from .forms import ChecklistItemForm
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import io
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils.encoding import smart_str
from auditlog.models import LogEntry
from rest_framework import status
from django.apps import apps
from django.contrib.auth.models import User
from collections import defaultdict
import datetime

# Create your views here.
@login_required
def checklist_view(request):
    """
    Main checklist view for displaying and managing user's checklist items.
    
    This view handles both GET and POST requests for the checklist page:
    - GET: Displays the checklist form and user's existing items
    - POST: Processes form submission for creating/updating checklist items
    
    URL Parameters:
    - edit: ID of checklist item to edit (optional)
    - highlight: Field to highlight in the form (optional, e.g., 'notes')
    
    Args:
        request: Django HttpRequest object containing user session and form data
        
    Returns:
        HttpResponse: Rendered checklist template with form and items context
    """
    user = request.user
    edit_id = request.GET.get('edit')
    highlight = request.GET.get('highlight')
    
    # Get the item to edit if edit_id is provided
    if edit_id:
        item_to_edit = get_object_or_404(ChecklistItem, id=edit_id, user=user)
    else:
        item_to_edit = None

    if request.method == 'POST':
        # Handle form submission for creating or updating checklist items
        if item_to_edit:
            form = ChecklistItemForm(request.POST, instance=item_to_edit, user=user)
        else:
            form = ChecklistItemForm(request.POST, user=user)
            
        if form.is_valid():
            checklist_item = form.save(commit=False)
            checklist_item.user = user
            checklist_item.save()
            
            # Display success message based on operation type
            if item_to_edit:
                messages.success(request, 'Checklist item updated successfully!')
            else:
                messages.success(request, 'Checklist item submitted successfully!')
            return redirect('checklist_page')
    else:
        # Handle GET request - display form and existing items
        form = ChecklistItemForm(instance=item_to_edit, user=user) if item_to_edit else ChecklistItemForm(user=user)
        
        # Highlight specific field if requested (e.g., for user guidance)
        if highlight == 'notes':
            form.fields['notes'].widget.attrs['style'] = 'background: #fffbe6; border: 2px solid #ffd700;'
    
    # Get user's checklist items with optimized query using select_related
    items = ChecklistItem.objects.filter(user=user).select_related('regulation_update').order_by('-last_updated')
    
    return render(request, 'checklist/index.html', {'form': form, 'items': items, 'item_to_edit': item_to_edit})

def index(request):
    """
    Simple index view that renders the checklist template.
    
    This is a basic view that serves the main checklist page without
    any specific functionality - used as a fallback or landing page.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        HttpResponse: Rendered checklist template
    """
    return render(request, 'checklist/index.html')

class RegulationUpdateViewSet(viewsets.ModelViewSet):
    """
    REST API ViewSet for managing regulation updates.
    
    Provides full CRUD operations for regulation updates through the API.
    Uses JWT authentication and includes comprehensive serialization.
    
    Attributes:
        queryset: Empty queryset (overridden in get_queryset)
        serializer_class: RegulationUpdateSerializer for API serialization
        permission_classes: Requires JWT authentication
    """
    queryset = RegulationUpdate.objects.none()  # Dummy queryset for router
    serializer_class = RegulationUpdateSerializer
    permission_classes = [IsAuthenticated]

class ChecklistItemViewSet(viewsets.ModelViewSet):
    """
    REST API ViewSet for managing checklist items.
    
    Provides full CRUD operations for checklist items with user-specific
    filtering. Staff users can see all items, regular users see only their own.
    
    Attributes:
        queryset: Empty queryset (overridden in get_queryset)
        serializer_class: ChecklistItemSerializer for API serialization
        permission_classes: Requires JWT authentication
    """
    queryset = ChecklistItem.objects.none()  # Dummy queryset for router
    serializer_class = ChecklistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get queryset filtered by user permissions.
        
        Staff users can access all checklist items, while regular users
        can only access their own items. Results are ordered by last_updated.
        
        Returns:
            QuerySet: Filtered and ordered checklist items
        """
        user = self.request.user
        if user.is_staff:
            return ChecklistItem.objects.all().order_by('-last_updated')
        return ChecklistItem.objects.filter(user=user).order_by('-last_updated')

    def create(self, request, *args, **kwargs):
        """
        Create a new checklist item via API.
        
        Handles POST requests to create new checklist items with proper
        error handling and logging. Validates data through serializer
        before saving to database.
        
        Args:
            request: HTTP request containing checklist item data
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Response: JSON response with created item data or error details
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        except Exception as exc:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"ChecklistItem create error: {exc}", exc_info=True)
            return Response({'detail': str(exc)}, status=400)

    def update(self, request, *args, **kwargs):
        """
        Update an existing checklist item via API.
        
        Handles PUT/PATCH requests to update existing checklist items.
        Supports partial updates and includes comprehensive error handling.
        
        Args:
            request: HTTP request containing updated item data
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments (partial update flag)
            
        Returns:
            Response: JSON response with updated item data or error details
        """
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as exc:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"ChecklistItem update error: {exc}", exc_info=True)
            return Response({'detail': str(exc)}, status=400)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_items_raw(self, request):
        """
        Custom API action to retrieve user's checklist items using raw SQL.
        
        This endpoint provides direct database access for performance-critical
        operations. Uses raw SQL to bypass ORM overhead and return data
        in a simplified format.
        
        Args:
            request: HTTP request with authenticated user
            
        Returns:
            Response: JSON response containing list of user's checklist items
        """
        user_id = request.user.id
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, completed, notes, last_updated, regulation_update_id FROM checklist_checklistitem WHERE user_id = %s",
                [user_id]
            )
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return Response(results)

class ComplianceReportView(APIView):
    """
    API view for generating compliance reports.
    
    Provides comprehensive compliance reporting including completion statistics,
    risk assessment data, and detailed item information for authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Generate a comprehensive compliance report for the authenticated user.
        
        Calculates completion statistics, risk assessments, and provides
        detailed information about all user's checklist items. Includes
        error handling for robust reporting.
        
        Args:
            request: HTTP request with authenticated user
            
        Returns:
            Response: JSON response containing compliance report data
        """
        try:
            user = request.user
            
            # Calculate completion statistics
            total = ChecklistItem.objects.filter(user=user).count()
            completed = ChecklistItem.objects.filter(user=user, completed=True).count()
            percent = (completed / total * 100) if total > 0 else 0
            
            # Build detailed risk information for each checklist item
            risks = [
                {
                    'id': item.id,
                    'regulation': item.regulation_update.title if item.regulation_update else None,
                    'completed': item.completed,
                    'likelihood': item.likelihood,
                    'impact': item.impact,
                    'notes': item.notes,
                    'admin_notes': item.admin_notes,
                }
                for item in ChecklistItem.objects.filter(user=user).select_related('regulation_update')
            ]
            
            return Response({
                'user': user.username,
                'total_items': total,
                'completed_items': completed,
                'completion_percentage': round(percent, 2),
                'risks': risks,
            })
        except Exception as e:
            return Response(
                {'error': 'Failed to generate compliance report', 'details': str(e)},
                status=500
            )

@login_required
def compliance_report_view(request):
    """
    Web-based compliance report view with filtering and export capabilities.
    
    Provides a comprehensive compliance report interface with support for:
    - Status filtering (completed/incomplete)
    - Risk level filtering (likelihood/impact)
    - Sorting options
    - Export formats (PDF, CSV)
    
    Args:
        request: Django HttpRequest with user session and query parameters
        
    Returns:
        HttpResponse: Rendered compliance report template or file download
    """
    user = request.user
    
    # Calculate basic completion statistics
    total = ChecklistItem.objects.filter(user=user).count()
    completed = ChecklistItem.objects.filter(user=user, completed=True).count()
    percent = (completed / total * 100) if total > 0 else 0
    
    # Build detailed risk information for each checklist item
    risks = [
        {
            'id': item.id,
            'regulation': item.regulation_update.title if item.regulation_update else None,
            'completed': item.completed,
            'likelihood': item.likelihood,
            'impact': item.impact,
            'notes': item.notes,
            'admin_notes': item.admin_notes,
        }
        for item in ChecklistItem.objects.filter(user=user).select_related('regulation_update')
    ]
    # Filtering
    status = request.GET.get('status')
    if status == 'completed':
        risks = [r for r in risks if r['completed']]
    elif status == 'incomplete':
        risks = [r for r in risks if not r['completed']]
    likelihood = request.GET.get('likelihood')
    if likelihood:
        risks = [r for r in risks if str(r['likelihood']) == str(likelihood)]
    impact = request.GET.get('impact')
    if impact:
        risks = [r for r in risks if str(r['impact']) == str(impact)]
    # Sorting
    sort = request.GET.get('sort')
    order = request.GET.get('order', 'asc')
    if sort in ['regulation', 'completed', 'likelihood', 'impact', 'notes', 'admin_notes']:
        risks = sorted(risks, key=lambda r: r[sort], reverse=(order=='desc'))
    context = {
        'user': user,
        'total_items': total,
        'completed_items': completed,
        'completion_percentage': round(percent, 2),
        'risks': risks,
        'request': request,
        'sort': sort,
        'order': order,
    }
    if request.GET.get('format') == 'pdf':
        template = get_template('checklist/compliance_report.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="compliance_report.pdf"'
        pisa.CreatePDF(html, dest=response)
        return response
    if request.GET.get('format') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="compliance_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Regulation', 'Status', 'Likelihood', 'Impact', 'Notes', 'Admin Notes'])
        for r in risks:
            writer.writerow([
                smart_str(r['regulation']),
                'Completed' if r['completed'] else 'Incomplete',
                r['likelihood'],
                r['impact'],
                smart_str(r['notes'] or '-'),
                smart_str(r['admin_notes'] or '-')
            ])
        return response
    return render(request, 'checklist/compliance_report.html', context)

class AuditLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, model_name, object_id):
        # Only allow certain models
        allowed_models = {'checklistitem': 'ChecklistItem', 'regulationupdate': 'RegulationUpdate'}
        if model_name.lower() not in allowed_models:
            return Response({'detail': 'Invalid model.'}, status=status.HTTP_400_BAD_REQUEST)
        model = apps.get_model('checklist', allowed_models[model_name.lower()])
        try:
            obj = model.objects.get(pk=object_id)
        except model.DoesNotExist:
            return Response({'detail': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Only allow access to own checklist items
        if model_name.lower() == 'checklistitem' and obj.user != request.user:
            return Response({'detail': 'Forbidden.'}, status=status.HTTP_403_FORBIDDEN)
        log_entries = LogEntry.objects.get_for_object(obj).order_by('-timestamp')
        data = [
            {
                'timestamp': entry.timestamp,
                'actor': entry.actor.username if entry.actor else None,
                'changes': entry.changes_dict,
                'action': entry.get_action_display(),
                'remote_addr': entry.remote_addr,
            }
            for entry in log_entries
        ]
        return Response(data)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
    def put(self, request):
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        user.save()
        return Response({'detail': 'Profile updated.'})

@login_required
def checklist_export_csv(request):
    """Export checklist items as CSV file."""
    user = request.user
    if user.is_staff:
        items = ChecklistItem.objects.all()
    else:
        items = ChecklistItem.objects.filter(user=user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="checklist.csv"'
    writer = csv.writer(response)
    writer.writerow(['User', 'Regulation', 'Completed', 'Notes', 'Mitigation Steps', 'Last Updated', 'Likelihood', 'Impact'])
    for item in items:
        writer.writerow([
            item.user.username,
            item.regulation_update.title if item.regulation_update else '',
            'Yes' if item.completed else 'No',
            item.notes or '',
            item.mitigation_steps or '',
            item.last_updated,
            item.likelihood,
            item.impact
        ])
    return response

@login_required
def checklist_export_pdf(request):
    """Export checklist items as PDF file."""
    user = request.user
    if user.is_staff:
        items = ChecklistItem.objects.all()
    else:
        items = ChecklistItem.objects.filter(user=user)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40
    p.setFont('Helvetica-Bold', 14)
    p.drawString(40, y, 'Checklist Report')
    y -= 30
    p.setFont('Helvetica', 10)
    for item in items:
        if y < 60:
            p.showPage()
            y = height - 40
        p.drawString(40, y, f"User: {item.user.username} | Regulation: {item.regulation_update.title if item.regulation_update else ''}")
        y -= 14
        p.drawString(60, y, f"Completed: {'Yes' if item.completed else 'No'} | Likelihood: {item.likelihood} | Impact: {item.impact}")
        y -= 14
        p.drawString(60, y, f"Notes: {item.notes or '-'}")
        y -= 14
        p.drawString(60, y, f"Mitigation Steps: {item.mitigation_steps or '-'}")
        y -= 20
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="checklist.pdf"'
    return response

# Keep the API views for API usage
class ChecklistExportCSV(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.is_staff:
            items = ChecklistItem.objects.all()
        else:
            items = ChecklistItem.objects.filter(user=user)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="checklist.csv"'
        writer = csv.writer(response)
        writer.writerow(['User', 'Regulation', 'Completed', 'Notes', 'Mitigation Steps', 'Last Updated', 'Likelihood', 'Impact'])
        for item in items:
            writer.writerow([
                item.user.username,
                item.regulation_update.title if item.regulation_update else '',
                'Yes' if item.completed else 'No',
                item.notes or '',
                item.mitigation_steps or '',
                item.last_updated,
                item.likelihood,
                item.impact
            ])
        return response

class ChecklistExportPDF(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.is_staff:
            items = ChecklistItem.objects.all()
        else:
            items = ChecklistItem.objects.filter(user=user)
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 40
        p.setFont('Helvetica-Bold', 14)
        p.drawString(40, y, 'Checklist Report')
        y -= 30
        p.setFont('Helvetica', 10)
        for item in items:
            if y < 60:
                p.showPage()
                y = height - 40
            p.drawString(40, y, f"User: {item.user.username} | Regulation: {item.regulation_update.title if item.regulation_update else ''}")
            y -= 14
            p.drawString(60, y, f"Completed: {'Yes' if item.completed else 'No'} | Likelihood: {item.likelihood} | Impact: {item.impact}")
            y -= 14
            p.drawString(60, y, f"Notes: {item.notes or '-'}")
            y -= 14
            p.drawString(60, y, f"Mitigation Steps: {item.mitigation_steps or '-'}")
            y -= 20
        p.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="checklist.pdf"'
        return response

class ReportTrendsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.is_staff:
            items = ChecklistItem.objects.all()
        else:
            items = ChecklistItem.objects.filter(user=user)
        # Example: completed vs incomplete over time (by month)
        trend = defaultdict(lambda: {'completed': 0, 'incomplete': 0})
        for item in items:
            month = item.last_updated.strftime('%Y-%m')
            if item.completed:
                trend[month]['completed'] += 1
            else:
                trend[month]['incomplete'] += 1
        # Sort by month
        trend_data = [
            {'month': m, 'completed': v['completed'], 'incomplete': v['incomplete']}
            for m, v in sorted(trend.items())
        ]
        return Response(trend_data)
