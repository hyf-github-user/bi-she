import request from '@/utils/request'

// 添加批量
export function addComment(data) {
  return request({
    url: '/blog/comment/',
    method: 'post',
    data
  })
}

// 删除单个评论
export function deleteComment(id) {
  return request({
    url: `/blog/comment/${id}/`,
    method: 'delete',
    params: { id }
  })
}

//  批量删除评论
export function deleteComments(ids) {
  return request({
    url: '/blog/comment/',
    method: 'delete',
    data: { 'ids': ids }
  })
}

// 更新评论信息
export function updateComment(id, data) {
  return request({
    url: `/blog/comment/${id}/`,
    method: 'put',
    data
  })
}

// 获取所有评论
export function getComments(data) {
  return request({
    url: '/blog/comment/',
    method: 'get',
    params: data
  })
}

// 根据某个id获取评论
export function getById(id) {
  return request({
    url: `/blog/comment/${id}/`,
    method: 'get'
  })
}

