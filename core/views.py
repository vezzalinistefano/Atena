import logging

from django.contrib.auth.forms import UserCreationForm
from django.http import FileResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

_logger = logging.getLogger(__name__)


class Maintenance(TemplateView):
    template_name = 'maintenance.html'


class NotFound(TemplateView):
    template_name = '404.html'


class Homepage(TemplateView):
    template_name = 'home.html'


class AccessForbidden(TemplateView):
    template_name = 'permission_denied.html'


class UserCreationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/user_create.html'
    success_url = reverse_lazy('homepage')


def media_access(request, path):
    """
    Manage media access through url
    """
    access_granted = False
    print('inside')
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            # If admin, everything is granted
            access_granted = True
        else:
            pass
            # TODO pensare se vietare a tutti l'accesso tramite url oppure no
            #  For simple user, only their documents can be accessed
            # doc = user.related_PRF_user.i_image  # Customize this...
            #
            # path = f"images/{path}"
            # if path == doc:
            #     access_granted = True

    if access_granted:
        response = FileResponse(user.related_PRF_user.i_image)
        return response
    else:
        return HttpResponseForbidden('Not authorized to access this media like this')
