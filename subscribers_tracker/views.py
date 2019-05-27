from django.shortcuts import render
from django.http import HttpResponse
from .models import User
import vk_api


def index(request):
    subscribers_new = get_all_subscribers('shadren808')
    subscribers_old = User.objects.all()
    subscribed = list(set(subscribers_new) - set(subscribers_old))
    unsubscribed = list(set(subscribers_old) - set(subscribers_new))
    context = {
        'subscribed': subscribed,
        'unsubscribed': unsubscribed,
        'all_subscribers': subscribers_new
    }
    User.objects.all().delete()
    User.objects.bulk_create(subscribers_new)
    return render(request, 'subscribers_tracker/index.html', context)


def get_all_subscribers(group_id):
    vk_session = vk_api.VkApi(app_id=5743772,
                              token='9f80a4009f80a4009f80a400e19fd7009c99f809f80a400c5fc0f1a903421384f8fad84',
                              api_version='5.95')
    vk = vk_session.get_api()
    user_ids = []
    count_per_request = 1000
    offset = 0
    while True:
        response = vk.groups.getMembers(group_id=group_id, count=count_per_request, offset=offset)
        user_ids.extend(response['items'])
        offset += count_per_request
        if len(response['items']) < count_per_request:
            break

    users = []
    offset = 0
    while True:
        response = vk.users.get(
            user_ids=str(user_ids[offset:offset + count_per_request])[1:-1])
        users.extend(list(map(lambda u: User(first_name=u['first_name'],
                                             last_name=u['last_name'],
                                             id=u['id']), response)))
        offset += count_per_request
        if len(response) < count_per_request:
            break

    return users
