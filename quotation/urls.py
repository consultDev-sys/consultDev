from django.urls import path

from quotation.views import BusinessView, EmiratesView, FreezoneView, QuotationView, PackageView

urlpatterns = [
    path('emirates/', EmiratesView.as_view(), name='quotation-api'),
    path('freezones/<int:emirate_id>/', FreezoneView.as_view(), name='freezone-api'),
    path('businesses/<int:emirate_id>/<int:freezone_id>/', BusinessView.as_view(), name='business-api'),
    path('packages/<int:emirate_id>/<int:freezone_id>/<int:business_id>/', PackageView.as_view(), name='business-api'),
    path('generate/', QuotationView.as_view(), name='quotation-api')
]

app_name = "quotation"