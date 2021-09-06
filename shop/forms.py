from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from shop.models import Course, Purchase, Comment, Review
from shop.validators import FileValidator


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


class CourseUploadForm(forms.Form):
    helper = FormHelper()
    helper.form_id = 'upload_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Add'))
    helper.inputs[0].field_classes = 'btn btn-success'

    title = forms.CharField(label='Course title', max_length=Course.MAX_LENGTH, min_length=Course.MIN_LENGTH)
    price = forms.FloatField(label='Price', initial=1.0, min_value=0.1)
    description = forms.CharField(widget=forms.Textarea, min_length=10)
    category = forms.ChoiceField(choices=Course.CATEGORY_CHOICES)

    file_validator = FileValidator(
        max_size=5 * (10 ** 7),
        content_types=('video/mp4',))
    video = forms.FileField(required=True,
                            validators=[file_validator])


class CourseUpdateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'add_comment_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Update'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Course
        fields = (
            'title',
            'price',
            'description'
        )


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


class AddReviewForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'add_review_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Add Review'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Review
        fields = [
            'vote',
            'body',
        ]


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
