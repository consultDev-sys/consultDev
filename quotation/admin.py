from django.contrib import admin

from quotation.forms import QuotationAdminForm
from quotation.models import Emirate, Freezone, BusinessActivity, BusinessInFreezone, FreezoneInEmirates, Quotation, VisaPackage, VisaPackagesInBusiness
from .forms import QuotationAdminForm

class QuotationAdmin(admin.ModelAdmin):
    form = QuotationAdminForm

    def get_readonly_fields(self, request, obj=None):
        return ['total_amount']
    
# Register your models here.
admin.site.register(Emirate)
admin.site.register(Freezone)
admin.site.register(BusinessActivity)
admin.site.register(VisaPackage)
admin.site.register(FreezoneInEmirates)
admin.site.register(BusinessInFreezone)
admin.site.register(Quotation)
admin.site.register(VisaPackagesInBusiness)
