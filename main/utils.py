from main.models import History


def add_to_history(object, request):
    from datetime import datetime
    created = datetime.now()
    user = request.user
    if user.is_authenticated:
        history = History.objects.get_or_create(user=user, movie=object)[0]
        history.created = created
        history.save()
