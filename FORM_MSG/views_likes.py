from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import BaseUpdateView

from FORM_MSG.models import Like, Message


# Django
class UpdateLikeView(LoginRequiredMixin, BaseUpdateView):
    model = Like

    def post(self, request, *args, **kwargs):
        msg: Message = get_object_or_404(klass=Message.objects.only('id'), id=self.kwargs['pk'])
        like, is_created = Like.objects.get_or_create(user=self.request.user, message=msg)  # returns all fields
        if not is_created:
            like.delete()
        return redirect(reverse('form_msg:msg_list'))


