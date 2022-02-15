/* eslint-disable no-prototype-builtins */
import { asyncRoutes, constantRoutes } from '@/router'

/**
 * Use meta.role to determine if the current user has permission
 * @param roles
 * @param route
 */
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
export function filterAsyncRoutes(routes, roles) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(roles, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, roles)
      }
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
        // var role_route = []
        // // 进行异步数组的过滤
        // asyncRoutes.forEach((item) => {
        //   // 对路由进行权限筛选
        //   if (item.hasOwnProperty('meta')) {
        //     if (item.meta.hasOwnProperty('roles')) {
        //       if (item.meta.roles.includes('admin')) {
        //         role_route.push(item)
        //       }
        //     }
        //   }
        // })
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
