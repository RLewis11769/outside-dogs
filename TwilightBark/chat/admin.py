""" Define admin panel for chat room system """
from django.contrib import admin
from django.core.paginator import Paginator
from django.core.cache import cache
from .models import ChatRoom, ChatMessage


class ChatRoomAdmin(admin.ModelAdmin):
    """ Define admin panel section for chat rooms """
    list_display = ['id', 'name']
    search_fields = ['name']
    readonly_fields = ['id']

    class Meta:
        model = ChatRoom


admin.site.register(ChatRoom, ChatRoomAdmin)


class CachingPaginator(Paginator):
    """ Custom paginator to cache results so all don't show up in admin """

    def _get_count(self):
        """ Get count of objects """
        if not hasattr(self, "_count"):
            self._count = None
        if self._count is None:
            try:
                # Set key to cache count
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)
            except:
                self._count = len(self.object_list)
            return self._count

    count = property(_get_count)


class ChatMessageAdmin(admin.ModelAdmin):
    """ Define admin panel section for chat messages """
    list_display = ['room', 'user', 'timestamp']
    list_filter = ['room', 'user', 'message', 'timestamp']
    search_fields = ['user__username', 'room__name']
    readonly_fields = ['id', 'user', 'room', 'timestamp']

    show_full_result_count = False
    paginator = CachingPaginator

    class Meta:
        model = ChatMessage


admin.site.register(ChatMessage, ChatMessageAdmin)
