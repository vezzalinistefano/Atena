from django import forms
from shop.models import Course, TeacherProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CourseForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'course_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Course
        fields = [
            'author',
            'title',
            'description',
            'price',
            'url'
        ]


class TeacherProfileForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'course_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = TeacherProfile
        fields = ['first_name', 'last_name', 'email', 'short_bio']


def form_validation_error(form):
    msg = ''
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)

    return msg
