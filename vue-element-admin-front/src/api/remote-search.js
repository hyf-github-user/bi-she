import request from '@/utils/request'

export function searchUser(name) {
  return request({
    url: '/data/search/user',
    method: 'get',
    params: { name }
  })
}

export function blogData(query) {
  return request({
    url: '/blog/data/',
    method: 'get',
    params: query
  })
}
