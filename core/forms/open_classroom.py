from django.forms import forms, Select

from core.forms.fields import CustomLabelModelChoiceField
from core.utils.references import HWCentralOpen


class OpenClassRoomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OpenClassRoomForm, self).__init__(*args, **kwargs)

        self.fields['grade'] = CustomLabelModelChoiceField(lambda x: str(x.pk), widget=Select(
            attrs={'class': 'hidden', 'id': 'new-grade-select'}),
                                                           queryset=HWCentralOpen.refs.CLASSROOMS,
                                                           help_text="Select the classroom you want to shift to.")
