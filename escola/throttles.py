from rest_framework.throttling import SimpleRateThrottle


class BaseRateThrottle(SimpleRateThrottle):
    def get_cache_key(self, request, view):
        return self.get_ident(request)


class EstudanteRateThrottle(BaseRateThrottle):
    rate = "20/day"


class CursoRateThrottle(BaseRateThrottle):
    rate = "10/day"
