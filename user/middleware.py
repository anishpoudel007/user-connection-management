# yourapp/middleware.py


def debug_request_middleware(get_response):
    def middleware(request):
        print("📦 Request Path:", request.path)
        print("🔍 Request Headers:", request.headers)
        print("\n")
        response = get_response(request)
        return response

    return middleware
