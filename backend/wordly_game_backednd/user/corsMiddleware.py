from django.http import HttpRequest, HttpResponse


def cors_middleware(get_response):
    def middleware(request: HttpRequest):
        if request.method == 'OPTIONS':
            r = HttpResponse()
            r['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
            r['Access-Control-Allow-Headers'] = 'Content-Type'
            r['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, HEAD'
            r['Access-Control-Allow-Credentials'] = 'true'
            return r

        response1 = get_response(request)
        response1['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
        response1['Access-Control-Allow-Headers'] = '*'
        response1['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, HEAD'
        response1['Access-Control-Allow-Credentials'] = 'true'
        return response1
    return middleware
