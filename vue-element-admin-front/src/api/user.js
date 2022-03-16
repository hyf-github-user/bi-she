import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/oauth/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/oauth/info/',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/oauth/logout/',
    method: 'post'
  })
}

// 获取所有用户
export function getUsers(page, size) {
  return request({
    url: '/user/UserList',
    method: 'get',
    params: { page, size }
  })
}

// 根据某个id获取用户
export function getById(id) {
  return request({
    url: '/user/getById',
    method: 'get',
    params: { id }
  })
}

// 添加用户信息
export function addUser(data) {
  return request({
    url: '/user/addUser',
    method: 'post',
    data
  })
}

// 更新用户信息
export function updateUser(data) {
  return request({
    url: '/user/updateUser',
    method: 'put',
    data
  })
}

// 删除用户信息
export function deleteUser(id) {
  return request({
    url: '/user/deleteUser',
    method: 'delete',
    params: { id }
  })
}

