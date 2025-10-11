import time
from django.utils.deprecation import MiddlewareMixin

class RequestTimingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if request.path == '/':
            total_time = time.time() - getattr(request, 'start_time', time.time())
            print(f"🏁 Home page loaded in {total_time:.3f} seconds.")
        return response
