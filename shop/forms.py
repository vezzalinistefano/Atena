from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from shop.models import Course, Purchase, Comment


class CourseForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'course_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'price',
            'category',
            'video'
        ]


class PurchaseForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'purchase_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Complete purchase'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Purchase
        exclude = [
            'buyer',
            'course_bought',
            'date',
        ]


class AddCommentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'add_comment_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Add'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Comment
        fields = [
            'body',
        ]


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
