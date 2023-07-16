from ipware import get_client_ip


class SetIPMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request=request)
        if ip is not None:
            request.META["HTTP_X_FORWARDED_FOR"] = ip
            request.META["REMOTE_ADDR"] = ip

        return self.get_response(request)
