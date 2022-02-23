from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from forum.models import Comment, CommentReply
from shop.models import Review


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


class AddReplyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'add_reply_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Add'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = CommentReply
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


class UpdateReviewForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'add_review_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Update Review'))
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
