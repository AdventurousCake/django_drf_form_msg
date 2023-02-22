import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from core.models import User
from .forms import MsgForm, CreationFormUser, CommentForm
from .models import Message, Comment

# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class UserDetails(DetailView):
    template_name = 'form_msg/USERPAGE.html'
    queryset = User.objects.all().select_related()

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk', '')
        context = super().get_context_data(**kwargs)
        query = Message.objects.select_related('author').values('id', 'author__username', 'text', 'created_date') \
            .order_by('-created_date') \
            .filter(author__id=pk)

        context['msgs_data'] = query
        context['msgs_data_count'] = query.count()
        return context


class SignUp(CreateView):
    form_class = CreationFormUser
    success_url = reverse_lazy("login")  # reverse_lazy("form_msg:msg_list")
    template_name = "form_msg/signup.html"


class MsgList(ListView):
    """List of messages with user likes"""
    template_name = "form_msg/msg_list.html"
    paginate_by = 2
    queryset = Message.objects.select_related('author').prefetch_related('likes')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MsgList, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            msgs = self.queryset
            context['show_buttons'] = True
            # likes_count in template

            # user likes msg ids
            context['user_likes'] = msgs.filter(likes__user=self.request.user.id).values_list('id', flat=True)
            print(context['user_likes'])
        return context

class DetailMsgView(DetailView):
    model = Message
    template_name = 'form_msg/msg_BY_ID.html'
    context_object_name = 'msg'

    def get_queryset(self):
        return get_object_or_404(klass=Message.objects.select_related("author", "comments")
                                 .values('id', 'author__username', 'text', 'created_date'),
                                 id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Message'
        context['is_detail_msg'] = True
        context['show_edit_buttons'] = self.object.get('author__username') == self.request.user.username
        return context


class DetailMsgANDCommentView(CreateView):
    model = Message
    template_name = 'form_msg/msg_BY_ID.html'
    context_object_name = 'msg'
    form_class = CommentForm

    queryset = Message.objects.select_related("author", "comments").values('id', 'author__username', 'text',
                                                                           'created_date')

    def get_success_url(self):
        return reverse_lazy('form_msg:show_msg', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        msg = self.get_object()
        context = super().get_context_data(**kwargs)
        context['title'] = 'Message'
        context['is_detail_msg'] = True
        context['show_edit_buttons'] = msg.get('author__username') == self.request.user.username
        context['comments'] = Comment.objects.select_related('user').filter(message__id=msg.get('id')).values(
            'user__username', 'text')
        context['show_comments'] = True
        context['msg'] = msg
        return context

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            raise PermissionDenied()

        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.message = Message.objects.get(pk=self.kwargs['pk'])

        return super(DetailMsgANDCommentView, self).form_valid(form)


class UpdateMsgView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MsgForm

    template_name = "form_msg/msg_send.html"
    success_url = reverse_lazy('form_msg:send_msg')

    def get_object(self, *args, **kwargs):
        obj = super(UpdateMsgView, self).get_object(*args, **kwargs)
        if obj.author != self.request.user:
            raise PermissionDenied()  # or Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "📨 Send message form"
        context['btn_caption'] = "Send"
        context['table_data'] = Message.objects.select_related().order_by('-created_date')[:5]

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        return super(UpdateMsgView, self).form_valid(form)


class DeleteMsgView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('form_msg:send_msg')

    # ignore confirm template
    def get(self, request, *args, **kwargs):
        # return self.post(request, *args, **kwargs)
        return self.delete(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        obj = super(DeleteMsgView, self).get_object(*args, **kwargs)
        if obj.author != self.request.user:
            raise PermissionDenied()  # or Http404
        return obj


class MsgFormCreateView(LoginRequiredMixin, CreateView):
    form_class = MsgForm
    template_name = "form_msg/msg_send.html"
    initial = {'text': 'example'}
    success_url = reverse_lazy('form_msg:send_msg')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "📨 Send message form"
        context['btn_caption'] = "Send"
        context['table_data'] = Message.objects.select_related().order_by('-created_date')[:5]

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        return super(MsgFormCreateView, self).form_valid(form)