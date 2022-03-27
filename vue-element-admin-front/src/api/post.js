import request from '@/utils/request'

export function getPosts(query) {
  return request({
    url: '/blog/post/',
    method: 'get',
    params: query
  })
}

export function getById(id) {
  return request({
    url: `/blog/post/${id}`,
    method: 'get'
  })
}

export function createPost(data) {
  return request({
    url: '/blog/post/',
    method: 'post',
    data
  })
}

// 删除单个文章信息
export function deletePost(id) {
  return request({
    url: `/blog/post/${id}/`,
    method: 'delete',
    params: { id }
  })
}

//  批量删除用户
export function deletePosts(ids) {
  return request({
    url: '/blog/post/',
    method: 'delete',
    data: { 'ids': ids }
  })
}

export function updatePost(id, data) {
  return request({
    url: `/blog/post/${id}/`,
    method: 'put',
    data
  })
}
