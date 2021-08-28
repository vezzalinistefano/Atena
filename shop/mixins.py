from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class OwnershipMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        if self.request.user.id == self.kwargs['pk']:
            return True
        return False