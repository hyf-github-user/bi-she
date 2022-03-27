import json

from drf_vue_element_admin.myapps.oauth.models import Permissions


def redis_storage_permissions(redis_conn):
    permissions = Permissions.objects.values('id', 'method')
    # 如果还没有任何权限控制，直接跳过后续逻辑，以免报错
    if not permissions.exists():
        return None
    permissions_dict = dict()
    for permission in permissions:
        # 去除不可见字符
        method = str(permission.get('method')).replace('\u200b', '')
        _id = permission.get('id')

        permissions_dict[_id] = {
            'method': method,
            'id': _id,
        }
        permissions_dict[_id] = json.dumps(permissions_dict[_id])
    redis_conn.hmset('user_permissions_manage', permissions_dict)
