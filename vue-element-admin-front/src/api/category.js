import request from '@/utils/request'

// 添加批量
export function addCategory(data) {
  return request({
    url: '/blog/category/',
    method: 'post',
    data
  })
}

// 删除单个评论
export function deleteCategory(id) {
  return request({
    url: `/blog/category/${id}/`,
    method: 'delete',
    params: { id }
  })
}

//  批量删除评论
export function deleteCategories(ids) {
  return request({
    url: '/blog/category/',
    method: 'delete',
    data: { 'ids': ids }
  })
}

// 更新评论信息
export function updateategory(id, data) {
  return request({
    url: `/blog/category/${id}/`,
    method: 'put',
    data
  })
}

// 获取所有评论
export function getCategories(data) {
  return request({
    url: '/blog/category/',
    method: 'get',
    params: data
  })
}

// 根据某个id获取评论
export function getById(id) {
  return request({
    url: `/blog/category/${id}/`,
    method: 'get'
  })
}

