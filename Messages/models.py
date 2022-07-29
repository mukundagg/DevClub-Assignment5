from django.db import models
from django.utils import timezone

# Create your models here.
class Message(models.Model):
    title = models.CharField(default = "#", blank = 'True', max_length=300);
    uniquemsgno = models.IntegerField(default = 0);
    fromMsg = models.CharField(default = "#", blank = True, max_length = 12); # Can be someone's entry number or even course code
    toMsg = models.CharField(default = "#", blank = True, max_length = 12); # Can be someone's entry number or even course code
    content = models.CharField(max_length = 50000, blank = True);
    nextMsg = models.ForeignKey('self', null = True, blank = True, on_delete = models.CASCADE); # Linked-List
    datetimesent = models.DateTimeField(default = timezone.now);

    def __init__(self, *args, **kwargs):
        if not args:
            totnum = self._meta.model.objects.all().count(); # All message objects
            kwargs["uniquemsgno"] = totnum + 1;
        super().__init__(*args, **kwargs);

class Forum(models.Model):
    name = models.CharField(max_length = 100, unique = True, blank = True, default = "DefaultForum");
    forumMessages = models.ManyToManyField(Message, blank = True);