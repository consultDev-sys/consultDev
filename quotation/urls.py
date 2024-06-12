from django.urls import path

from quotation.views import BusinessView, EmiratesView, FreezoneView

urlpatterns = [
    path('emirates/', EmiratesView.as_view(), name="quotation-api"),
    path('freezone/<int:emirate_id>/', FreezoneView.as_view(), name="freezone-api"),
    path('business/<int:emirate_id>/<int:freezone_id>/', BusinessView.as_view(), name="business-api")
]

app_name = "quotation"