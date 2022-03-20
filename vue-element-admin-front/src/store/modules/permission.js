/* eslint-disable no-prototype-builtins */
import { asyncRoutes, constantRoutes } from '@/router'

/**
 * Use meta.role to determine if the current users has permission
 * @param roles
 * @param route
 */
// 判断这个路由是否有权限访问
function hasPermission(roles, route) {
  if (route.meta && route.meta.roles) {
    return roles.some(role => route.meta.roles.includes(role))
  } else {
    return true
  }
}

/**
 * Filter asynchronous routing tables by recursion
 * @param routes asyncRoutes
 * @param roles
 */
// 根据身份权限过滤动态路由
export function filterAsyncRoutes(routes, roles) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }

    if (hasPermission(roles, tmp)) {
      if (tmp.children) {
        // 进行递归过滤路由
        tmp.children = filterAsyncRoutes(tmp.children, roles)
      }
      console.log('tmp: ', tmp)
      res.push(tmp)
    }
  })

  return res
}

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  // 根据roles生成动态路由
  generateRoutes({ commit }, roles) {
    return new Promise(resolve => {
      let accessedRoutes
      // 判断当前的用户roles是否包含admin
      if (roles.includes('admin')) {
        // 所有的路由都可以被访问,将asyncRoutes进行改造成从数据库中获取从而实现前端的权限管理
        accessedRoutes = asyncRoutes || []
      } else {
        // 根据角色过滤不能访问的路由表
        accessedRoutes = filterAsyncRoutes(asyncRoutes, roles)
      }
      // 设置动态路由表
      commit('SET_ROUTES', accessedRoutes)
      resolve(accessedRoutes)
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
