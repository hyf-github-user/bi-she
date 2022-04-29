import store from '@/store'

/**
 * @param {Array} value
 * @returns {Boolean}
 * @posts see @/views/permission/directive.vue
 */
export default function checkPermission(value) {
  if (value && value instanceof Array && value.length > 0) {
    const roles = store.getters && store.getters.roles
    const permissionRoles = value

    const hasPermission = roles.some(role => {
      return permissionRoles.includes(role)
    })
    return hasPermission
  } else {
    console.error(`权限不足,请使用v-permission="['admin','editor']"进行更新路由权限`)
    return false
  }
}
