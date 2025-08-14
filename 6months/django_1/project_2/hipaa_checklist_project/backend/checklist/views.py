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

# Create your views here.
@login_required
def checklist_view(request):
    user = request.user
    edit_id = request.GET.get('edit')
    highlight = request.GET.get('highlight')
    if edit_id:
        item_to_edit = get_object_or_404(ChecklistItem, id=edit_id, user=user)
    else:
        item_to_edit = None

    if request.method == 'POST':
        if item_to_edit:
            form = ChecklistItemForm(request.POST, instance=item_to_edit)
        else:
            form = ChecklistItemForm(request.POST)
        if form.is_valid():
            checklist_item = form.save(commit=False)
            checklist_item.user = user
            checklist_item.save()
            if item_to_edit:
                messages.success(request, 'Checklist item updated successfully!')
            else:
                messages.success(request, 'Checklist item submitted successfully!')
            return redirect('checklist_page')
    else:
        form = ChecklistItemForm(instance=item_to_edit) if item_to_edit else ChecklistItemForm()
        # Highlight notes field if requested
        if highlight == 'notes':
            form.fields['notes'].widget.attrs['style'] = 'background: #fffbe6; border: 2px solid #ffd700;'
    items = ChecklistItem.objects.filter(user=user).select_related('regulation_update').order_by('-last_updated')
    return render(request, 'checklist/index.html', {'form': form, 'items': items, 'item_to_edit': item_to_edit})

def index(request):
    return render(request, 'checklist/index.html')

class RegulationUpdateViewSet(viewsets.ModelViewSet):
    queryset = RegulationUpdate.objects.none()  # Dummy queryset for router
    serializer_class = RegulationUpdateSerializer
    permission_classes = [IsAuthenticated]

class ChecklistItemViewSet(viewsets.ModelViewSet):
    queryset = ChecklistItem.objects.none()  # Dummy queryset for router
    serializer_class = ChecklistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChecklistItem.objects.filter(user=self.request.user).order_by('-last_updated')

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_items_raw(self, request):
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total = ChecklistItem.objects.filter(user=user).count()
        completed = ChecklistItem.objects.filter(user=user, completed=True).count()
        percent = (completed / total * 100) if total > 0 else 0
        return Response({
            'user': user.username,
            'total_items': total,
            'completed_items': completed,
            'completion_percentage': round(percent, 2),
        })
