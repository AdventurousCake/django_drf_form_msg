from rest_framework.throttling import UserRateThrottle


class OncePerDayUserThrottle(UserRateThrottle):
        rate = '1/day'