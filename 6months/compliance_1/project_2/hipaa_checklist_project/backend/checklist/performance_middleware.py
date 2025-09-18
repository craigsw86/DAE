"""
Performance middleware for HIPAA Checklist Project
"""

import time
from django.utils.deprecation import MiddlewareMixin

class PerformanceMiddleware(MiddlewareMixin):
    """Middleware to optimize performance"""
    
    def process_request(self, request):
        """Process request - start timing"""
        request.start_time = time.time()
    
    def process_response(self, request, response):
        """Process response - add performance headers"""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Response-Time'] = f"{duration:.3f}s"
            
            # Add caching headers for static content
            if request.path.startswith('/static/'):
                response['Cache-Control'] = 'public, max-age=31536000'  # 1 year
                response['Expires'] = 'Thu, 31 Dec 2025 23:59:59 GMT'
        
        return response
