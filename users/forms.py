from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm

from users.models import UserProfile


class RegisterForm(UserCreationForm):
    helper = FormHelper()
    helper.form_id = 'register_form'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'
    helper.form_method = 'POST'

    class Meta:
        model = UserProfile
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'user_photo',
            'is_teacher'
        )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_teacher = self.cleaned_data['is_teacher']
        user.user_photo = self.cleaned_data['user_photo']

        if commit:
            user.save()
        return user


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
