from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

"""
此工具类验证登录状态
"""

class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
