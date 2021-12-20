import Cookies from 'js-cookie'

const TokenKey = 'Admin-Token'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function get_Jwt_Token() {
  return Cookies.get(TokenKey)
}

export function set_Jwt_Token(token) {
  return Cookies.set(TokenKey, token)
}
