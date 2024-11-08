from django.shortcuts import render
from .models import DisasterStatistics, EmergencyResource

def landing_page(request):
    context = {
        'disaster_statistics': DisasterStatistics.objects.all()[:4],
        'emergency_resources': EmergencyResource.objects.filter(resource_type='Contact'),
    }
    return render(request, 'disaster_management/landing_page.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def dashboard(request):
    context = {
        'active_alerts_count': 0,  # Replace with actual query
        'shelters_count': 0,       # Replace with actual query
        'reports_count': 0,        # Replace with actual query
        'users_count': 0,          # Replace with actual query
    }
    
    if request.user.is_staff:
        context.update({
            'recent_incidents': [],  # Add your incidents query
        })
    else:
        context.update({
            'user_reports': [],      # Add user's reports query
            'nearby_shelters': [],   # Add nearby shelters query
        })
    
    return render(request, 'dashboard/dashboard.html', context)
