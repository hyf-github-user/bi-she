# 作者：我只是代码的搬运工
# coding:utf-8
class Scope:
    """
    身份类的基类
    """
    allow_module = ()  # 允许访问的模块名

    def __add__(self, other):
        # 对允许的视图函数进行相加
        self.allow_module = self.allow_module + other.allow_module
        return self


class user(Scope):
    """
    普通用户
    """
    allow_module = ()  # 允许访问的视图函数


class admin(Scope):
    """
    超级管理员
    """
    allow_module = ('UserList', 'getById', 'updateUser',
                    'deleteUser', 'addUser')  # 允许访问的视图函数

    # 加上协管员的身份权限

    def __init__(self):
        self + user()


def is_in_scope(scope, endpoint):
    scope = globals()[scope]()  # 根据scope获取SuperAdmin对象
    # 判断现在进入的视图函数是否为该身份能进入的
    if endpoint in scope.allow_module:
        return True
    else:
        return False
