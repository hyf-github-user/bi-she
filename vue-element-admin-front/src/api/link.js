import request from '@/utils/request'

// 添加批量
export function addLink(data) {
  return request({
    url: '/blog/link/',
    method: 'post',
    data
  })
}

// 删除单个评论
export function deleteLink(id) {
  return request({
    url: `/blog/link/${id}/`,
    method: 'delete',
    params: { id }
  })
}

//  批量删除评论
export function deleteLinks(ids) {
  return request({
    url: '/blog/link/',
    method: 'delete',
    data: { 'ids': ids }
  })
}

// 更新评论信息
export function updateLink(id, data) {
  return request({
    url: `/blog/link/${id}/`,
    method: 'put',
    data
  })
}

// 获取所有评论
export function getLinks(data) {
  return request({
    url: '/blog/link/',
    method: 'get',
    params: data
  })
}

// 根据某个id获取评论
export function getById(id) {
  return request({
    url: `/blog/link/${id}/`,
    method: 'get'
  })
}

