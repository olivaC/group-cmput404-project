class BaseContextMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.request = request
        self.context = dict()
        self.populate_context()
        self.request.context = self.context
        response = self.get_response(self.request)
        return response

    def populate_context(self):
        if self.request.user.is_authenticated:
            try:
                self.context['user_profile'] = self.request.user.profile
            except:
                pass
