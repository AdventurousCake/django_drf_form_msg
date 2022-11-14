# from django.conf import settings
from django.db import models
from core.models import User


# from django.utils import timezone
# class B_User(models.Model):
#     # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     id = models.IntegerField(unique=True, primary_key=True)
#     id_user = models.IntegerField()
#     name = models.CharField(max_length=100)
#     data = models.TextField()
#     created_date = models.DateTimeField(null=True)
#
#     # def publish(self):
#     #     self.published_date = timezone.now()
#     #     self.save()
#
#     class Meta:
#         ordering = ('id',)
#
#     def __str__(self):
#         return 'USER'+self.name

# class MessageBase(models.Model):
#     class Meta:
#         abstract = True
#
#     created_date = models.DateTimeField(null=False, auto_now_add=True)
#     updated_date = models.DateTimeField(null=False, auto_now=True)


class Message(models.Model):
    # o2m; blank true - не обяз. в форме (пусто)
    author = models.ForeignKey(to=User, related_name='messages', on_delete=models.CASCADE)
    id = models.BigAutoField(null=False, unique=True, primary_key=True,
                             auto_created=True)  # limit int remove (max_length)
    name = models.CharField(null=False, max_length=10, blank=False)
    text = models.TextField(null=False, max_length=100, blank=False)
    accept_terms = models.BooleanField(null=False, default=False, verbose_name='Согласен с правилами', blank=False)
    file = models.FileField(null=True, upload_to='form_files/', blank=True)
    image = models.ImageField(null=True, upload_to='form_imgs/', blank=True)

    created_date = models.DateTimeField(null=False, auto_now_add=True)
    updated_date = models.DateTimeField(null=False, auto_now=True)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     pass

    # python_field = None
    def msg_length(self):
        return len(self.text)

    def __str__(self):
        return f"{self.name} {self.text}"
