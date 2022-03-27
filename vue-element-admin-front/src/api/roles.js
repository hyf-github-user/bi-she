import request from '@/utils/request'

// 添加批量
export function addRole(data) {
  return request({
    url: '/blog/role/',
    method: 'post',
    data
  })
}

// 删除单个评论
export function deleteRole(id) {
  return request({
    url: `/blog/role/${id}/`,
    method: 'delete',
    params: { id }
  })
}

//  批量删除评论
export function deleteRoles(ids) {
  return request({
    url: '/blog/role/',
    method: 'delete',
    data: { 'ids': ids }
  })
}

// 更新评论信息
export function updateRole(id, data) {
  return request({
    url: `/blog/role/${id}/`,
    method: 'put',
    data
  })
}

// 获取所有评论
export function getRoles(data) {
  return request({
    url: '/blog/role/',
    method: 'get',
    params: data
  })
}

// 根据某个id获取评论
export function getById(id) {
  return request({
    url: `/blog/role/${id}/`,
    method: 'get'
  })
}

