"""
Custom security middleware for HIPAA Checklist Project
Adds comprehensive security headers for HIPAA compliance and security best practices
"""

class SecurityHeadersMiddleware:
    """
    Middleware to add comprehensive security headers for HIPAA compliance.
    
    This middleware implements defense-in-depth security by adding multiple
    layers of security headers to protect against common web vulnerabilities
    and ensure HIPAA compliance requirements are met.
    """
    
    def __init__(self, get_response):
        """
        Initialize the security middleware.
        
        Args:
            get_response: Django's get_response callable
        """
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Process the request and add security headers to the response.
        
        Applies comprehensive security headers to protect against:
        - Clickjacking attacks (X-Frame-Options)
        - MIME type sniffing (X-Content-Type-Options)
        - XSS attacks (X-XSS-Protection, CSP)
        - Man-in-the-middle attacks (HSTS)
        - Information leakage (Referrer-Policy)
        - Unauthorized resource access (CORS policies)
        
        Args:
            request: Django HttpRequest object
            
        Returns:
            HttpResponse: Response with security headers added
        """
        response = self.get_response(request)
        
        # Comprehensive security headers for HIPAA compliance
        security_headers = {
            # Prevent clickjacking attacks
            'X-Frame-Options': 'DENY',
            
            # Prevent MIME type sniffing
            'X-Content-Type-Options': 'nosniff',
            
            # Enable XSS protection
            'X-XSS-Protection': '1; mode=block',
            
            # Force HTTPS for 1 year (HIPAA requirement)
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            
            # Control referrer information leakage
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            
            # Content Security Policy to prevent XSS and injection attacks
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none';",
            
            # Restrict browser APIs to prevent unauthorized access
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=(), gyroscope=(), accelerometer=()',
            
            # Prevent cross-domain policy files
            'X-Permitted-Cross-Domain-Policies': 'none',
            
            # Cross-Origin policies for additional security
            'Cross-Origin-Embedder-Policy': 'require-corp',
            'Cross-Origin-Opener-Policy': 'same-origin',
            'Cross-Origin-Resource-Policy': 'same-origin',
        }
        
        # Add security headers to response (only if not already present)
        for header, value in security_headers.items():
            if header not in response:
                response[header] = value
        
        return response

