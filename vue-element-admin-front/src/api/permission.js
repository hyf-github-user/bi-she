import request from '@/utils/request'

// 添加批量
export function addPermission(data) {
  return request({
    url: '/blog/permission/',
    method: 'post',
    data
  })
}

// 删除单个评论
export function deletePermission(id) {
  return request({
    url: `/blog/permission/${id}/`,
    method: 'delete',
    params: { id }
  })
}

//  批量删除评论
export function deletePermissions(ids) {
  return request({
    url: '/blog/permission/',
    method: 'delete',
    data: { 'ids': ids }
  })
}

// 更新评论信息
export function updatePermission(id, data) {
  return request({
    url: `/blog/permission/${id}/`,
    method: 'put',
    data
  })
}

// 获取所有评论
export function getPermissions(data) {
  return request({
    url: '/blog/permission/',
    method: 'get',
    params: data
  })
}

// 根据某个id获取评论
export function getById(id) {
  return request({
    url: `/blog/permission/${id}/`,
    method: 'get'
  })
}

