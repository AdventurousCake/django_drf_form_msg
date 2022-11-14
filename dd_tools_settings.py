from django1.settings import *

# DEBUG = False
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
INSTALLED_APPS.append("debug_toolbar")

# debug tools ip
INTERNAL_IPS = [
    # localhost only
    "127.0.0.1",
]

# add to urlpatterns
# urlpatterns = [
#     path('__debug__/', include('debug_toolbar.urls')),
# ]