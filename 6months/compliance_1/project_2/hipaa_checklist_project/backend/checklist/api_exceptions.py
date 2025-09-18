from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Log all exceptions
    logger.error(f"Exception: {exc}", exc_info=True)

    if response is not None:
        # Add a 'detail' field if not present
        if 'detail' not in response.data:
            response.data['detail'] = str(exc)
        # Optionally, add the status code
        response.data['status_code'] = response.status_code
    else:
        # Handle non-DRF exceptions
        return Response({
            'detail': str(exc),
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
