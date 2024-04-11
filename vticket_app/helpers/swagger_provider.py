from drf_yasg import openapi

class SwaggerProvider():
    @staticmethod
    def header_authentication():
        return openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Authorization')
    
    @staticmethod
    def form_data(name: str, type: str, description: str = ""):
        return openapi.Parameter(name, in_=openapi.IN_FORM, type=type, description=description)