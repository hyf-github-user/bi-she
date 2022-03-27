import request from '@/utils/request'

// 添加批量
export function addNotification(data) {
  return request({
    url: '/blog/notification/',
    method: 'post',
    data
  })
}

// 删除单个评论
export function deleteNotification(id) {
  return request({
    url: `/blog/notification/${id}/`,
    method: 'delete',
    params: { id }
  })
}

//  批量删除评论
export function deleteNotifications(ids) {
  return request({
    url: '/blog/notification/',
    method: 'delete',
    data: { 'ids': ids }
  })
}

// 更新评论信息
export function updateNotification(id, data) {
  return request({
    url: `/blog/notification/${id}/`,
    method: 'put',
    data
  })
}

// 获取所有评论
export function getNotifications(data) {
  return request({
    url: '/blog/notification/',
    method: 'get',
    params: data
  })
}

// 根据某个id获取评论
export function getById(id) {
  return request({
    url: `/blog/notification/${id}/`,
    method: 'get'
  })
}

