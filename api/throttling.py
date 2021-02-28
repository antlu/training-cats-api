from rest_framework.throttling import SimpleRateThrottle


class AllUsersRateThrottle(SimpleRateThrottle):
    scope = 'all'

    def get_cache_key(self, request, view):
        return 'throttle_all'
