# 作者：我只是代码的搬运工
# coding:utf-8

class Scope:
    allow_api = ()  # 允许访问的视图函数
    allow_module = ()  # 允许访问的模块名
    forbidden = ()  # 禁止访问的视图函数

    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_module = self.allow_module + other.allow_module
        self.forbidden = self.forbidden + other.forbidden
        # self.allow_api = list(set(self.allow_api))  # 去重 allow_api再相加的时候会有重复，debug可以看到
        return self


# 普通用户
class user(Scope):
    allow_api = ()  # 允许访问的API
    allow_module = ('login',)  # 允许访问的视图函数
    forbidden = ()  # 禁止访问的视图函数


# 协管员
class editor(Scope):
    allow_api = ()  # 允许访问的API
    allow_module = ()  # 允许访问的视图函数

    def __init__(self):
        self + user()


# 超级管理员
class admin(Scope):
    allow_module = ()

    def __init__(self):
        self + editor()


def is_in_scope(scope, endpoint, module_name):
    scope = globals()[scope]()  # 根据scope获取SuperAdmin对象
    if endpoint in scope.forbidden:  # 判断这次的视图函数是否被禁止
        return False
    if endpoint in scope.allow_api:
        return True
    if module_name in scope.allow_module:
        return True
    else:
        return False
