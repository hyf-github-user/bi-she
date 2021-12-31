import request from '@/utils/request'

export function searchUser(name) {
  return request({
    url: '/data/search/user',
    method: 'get',
    params: { name }
  })
}

export function transactionList(query) {
  return request({
    url: '/data/transaction/list',
    method: 'get',
    params: query
  })
}
