import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        logger.error(f'Unhandled Server Exception: {exc}', exc_info=True)
        err_str = str(exc)
        if 'relation' in err_str.lower() and 'does not exist' in err_str.lower():
            err_msg = 'Database initialization in progress. Please retry.'
        else:
            err_msg = err_str if err_str else 'Internal server error occurred.'
            
        return Response(
            {
                'detail': err_msg,
                'error': 'InternalServerError'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
