__author__ = 'cltanuki'
import vk
from db_work.models import VkUser, VkUserInfo, soc_db

soc_db.connect()
soc_db.create_table(VkUserInfo, safe=True)

user_list = [str(u.id_str) for u in VkUser.select().limit(1000)]
vkapi = vk.API('4561834', 'Tanuki2007@gmail.com', 'mFox2672')
res = vkapi.users.get(user_ids=",".join(user_list), fields='sex, bdate, city, country, photo_50, online, , screen_name,'
                                                           'online_mobile, has_mobile, contacts, connections, '
                                                           'site, universities, schools, status, last_seen, '
                                                           'followers_count, relation, relatives, counters, '
                                                           'screen_name, occupation, activities, interests, music, '
                                                           'movies, tv, books, games, about, quotes, personal')

profile_fill_key_list = ['sex', 'city', 'country', 'home_town', 'contacts', 'connections', 'universities', 'schools',
                         'relation', 'occupation', 'activities', 'interests', 'music', 'movies', 'tv', 'books', 'games',
                         'about', 'quotes']

to_write_key_list = []

for user_dict in res:
    user = VkUser.get(id_str=user_dict['id'])
    if 'deactivated' in user_dict.keys():
        if user_dict['deactivated'] == 'banned':
            user.deactivated = 0
        else:
            user.deactivated = 1
        user.save()
        continue
    if 'personal' in user_dict.keys() and isinstance(user_dict['personal'], dict) \
            and 'lang' in user_dict['personal'].keys():
        if 'Русский' in user_dict['personal']:
            user.is_ru = True
        else:
            user.is_ru = False
    user_dict['profile_fill_count'] = 0
    for key in profile_fill_key_list:
        if key in user_dict.keys():
            user_dict['profile_fill_count'] += 5
    user_dict['added_media_count'] = user_dict['counters']['photos'] + user_dict['counters']['videos'] \
        if 'counters' in user_dict.keys() else -1
    user.save()
    user_dict['country'] = user_dict['country']['id'] if 'country' in user_dict.keys() else -1
    del user_dict['id']
    print(user_dict)
    VkUserInfo.create(user=user, **user_dict)