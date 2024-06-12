from django import forms
from .models import Quotation

class QuotationAdminForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = '__all__'
        widgets = {
            'total_amount': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_amount'].help_text = "Total will be calculated automatically after saving."
