import request from '@/utils/request'

// 添加用户信息
export function addUser(data) {
  return request({
    url: '/blog/users/',
    method: 'post',
    data
  })
}

// 删除单个用户信息
export function deleteUser(id) {
  return request({
    url: `/blog/users/${id}/`,
    method: 'delete',
    params: { id }
  })
}

//  批量删除用户
export function deleteUsers(ids) {
  return request({
    url: '/blog/users/',
    method: 'delete',
    data: { 'ids': ids }
  })
}

// 更新用户信息
export function updateUser(id, data) {
  return request({
    url: `/blog/users/${id}/`,
    method: 'put',
    data
  })
}

// 获取所有用户
export function getUsers(data) {
  return request({
    url: '/blog/users/',
    method: 'get',
    params: data
  })
}

// 根据某个id获取用户
export function getById(id) {
  return request({
    url: `/blog/users/${id}/`,
    method: 'get'
  })
}

