from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, View
from django.http import HttpResponse

from .forms import MessageForm
from .models import Notification
from application.survey.models import User, UserDevice


class MessageUsersCountView(View):

    def get(self, request):

        full_filter = {}

        full_filter['id__in'] = UserDevice.objects.values('user__id')
        
        if self.request.GET.get('id_user'):
            full_filter['id'] = self.request.GET.get('id_user')
        else:

            if self.request.GET.get('advisor'):
                full_filter['advisor__contains'] = self.request.GET.get('advisor')

            status_legal = self.request.GET.get('status_legal')
            if status_legal and (status_legal != 'all'):
                full_filter['status_legal'] = status_legal

            user_type = self.request.GET.get('user_type')
            if user_type and (user_type != 'all'):
                full_filter['type'] = user_type

            if self.request.GET.get('user_status'):
                full_filter['status'] = self.request.GET.get('user_status')

            if self.request.GET.get('rank'):
                full_filter['rank'] = self.request.GET.get('rank')
        
        users_list = User.objects.filter(**full_filter).all()
        users_count = len(users_list)

        return HttpResponse(users_count)


class MessageView(FormView):

    template_name = 'mobile/message.html'
    form_class = MessageForm
    success_url = reverse_lazy('mobile:message')

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(MessageView, self).get(request, *args, **kwargs)

    def form_valid(self, form):

        user_filter = {}
        user_filter['id__in'] = UserDevice.objects.values('user__id')

        full_filter = {}
        
        if form.cleaned_data.get('id_user'):
            full_filter['id'] = form.cleaned_data['id_user'].id
        else:
            if form.cleaned_data.get('advisor'):
                full_filter['advisor__contains'] = form.cleaned_data['advisor']

            status_legal = form.cleaned_data.get('status_legal')
            if status_legal and (status_legal != 'all'):
                full_filter['status_legal'] = status_legal
            user_type = form.cleaned_data.get('user_type')
            if user_type and (user_type != 'all'):
                full_filter['type'] = user_type

            if form.cleaned_data.get('user_status'):
                full_filter['status'] = form.cleaned_data['user_status']

            if form.cleaned_data.get('rank'):
                full_filter['rank'] = form.cleaned_data['rank']

        users_list = User.objects.filter(**user_filter, **full_filter).all()

        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        
        if full_filter:
            for user in users_list:
                notification = Notification()
                notification.user = user
                notification.title = title
                notification.message = message
                notification.category = 'important'
                notification.save()
        else:
            notification = Notification()
            notification.title = title
            notification.message = message
            notification.category = 'important'
            notification.save()

        messages.success(self.request, _('The message was successfully sent out'))

        return super(MessageView, self).form_valid(form)
