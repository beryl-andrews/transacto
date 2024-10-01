from django.urls import path, include

urlpatterns = [
    path('', include("users.urls")),
    path('account/', include("accounts.urls"))
]
