import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from users.models import UserProfile


class UserProfileForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'user_profile_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Update'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = UserProfile
        fields = (
            'username',
            'first_name',
            'last_name',
            'user_photo',
            'email',
            'bio'
        )

    def save(self, commit=True):
        profile_pic = UserProfile.objects.get(pk=self.instance.pk).user_photo
        instance = super().save(commit)
        if profile_pic != instance.user_photo:
            os.remove(f'media/{profile_pic}')


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
