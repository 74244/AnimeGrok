from src.articles.models import Viewer


class CountViewerMixin:

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

    #TODO: Переписать нормально функцию для анонимного пользователя
    def get_mixin_ip(self, request, *args, **kwargs):

        if hasattr(self.object, 'viewers') and request.user.is_authenticated:
            test = viewer, created = Viewer.objects.get_or_create(
                ip=None if request.user.is_authenticated else self.get_client_ip(request),
                user=request.user if request.user.is_authenticated else None
            )
            if self.object.viewers.filter(id=viewer.id).count() == 0:
                self.object.viewers.add(viewer)
            return viewer
        else:
            return self.get_client_ip(request)
