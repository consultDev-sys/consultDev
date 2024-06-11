from django.urls import path

urlpatterns = [
    path("", QuotationView.as_view(), name="quotation-api"),
]

app_name = "quotation"