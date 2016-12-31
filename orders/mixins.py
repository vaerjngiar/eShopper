from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .models import Order


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
