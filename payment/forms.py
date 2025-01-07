from django import forms
from unfold.widgets import UnfoldAdminDateWidget,UnfoldAdminSelectWidget

class TailwindBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "block w-full px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md focus:border-blue-500 focus:ring focus:ring-blue-300 focus:outline-none focus:ring-opacity-40"
            })


class PaymentCustomForm(forms.Form):
    start_date = forms.DateField(required=False, label="Boshlanish sanasi", widget=UnfoldAdminDateWidget(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, label="Tugash sanasi", widget=UnfoldAdminDateWidget(attrs={'type': 'date'}))


