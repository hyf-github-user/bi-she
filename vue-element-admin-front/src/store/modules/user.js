import { login, logout, getInfo } from '@/api/login'
import { getToken, setToken, removeToken } from '@/utils/auth'
import router, { resetRouter } from '@/router'

const state = {
  token: getToken(),
  name: '',
  username: '',
  avatar: '',
  introduction: '',
  roles: [],
  email: '',
  mobile: ''
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_USERNAME: (state, username) => {
    state.username = username
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_INTRODUCTION: (state, introduction) => {
    state.introduction = introduction
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  },
  SET_EMAIL: (state, email) => {
    state.email = email
  },
  SET_MOBILE: (state, mobile) => {
    state.mobile = mobile
  }
}

const actions = {
  // 用户登录
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    // 异步调用login的ajax方法
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { data } = response
        commit('SET_TOKEN', data.token)
        setToken(data.token)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 获取用户的身份信息
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        const { data } = response

        if (!data) {
          reject('认证失败,请重新登录!')
        }

        const { roles, name, username, avatar, introduction, email, mobile } = data
        // roles must be a non-empty array
        if (!roles || roles.length <= 0) {
          reject('getInfo: roles must be a non-null array!')
        }
        // 设置用户信息
        commit('SET_ROLES', roles)
        commit('SET_NAME', name)
        commit('SET_USERNAME', username)
        commit('SET_AVATAR', avatar)
        commit('SET_INTRODUCTION', introduction)
        commit('SET_EMAIL', email)
        commit('SET_MOBILE', mobile)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 用户退出登录
  logout({ commit, state, dispatch }) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        commit('SET_TOKEN', '')
        commit('SET_ROLES', [])
        removeToken()
        resetRouter()

        // reset visited views and cached views
        // to fixed https://github.com/PanJiaChen/vue-element-admin/issues/2485
        dispatch('tagsView/delAllViews', null, { root: true })

        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 移除token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('SET_TOKEN', '')
      commit('SET_ROLES', [])
      removeToken()
      resolve()
    })
  },

  // 动态地修改权限
  async changeRoles({ commit, dispatch }, role) {
    // const token = role + '-token'
    //
    // commit('SET_TOKEN', token)
    // setToken(token)

    const { roles } = await dispatch('getInfo')

    resetRouter()

    // 根据角色生成可访问路由图
    const accessRoutes = await dispatch('permission/generateRoutes', roles, { root: true })
    // 动态添加可访问路由
    router.addRoutes(accessRoutes)

    // 重置访问的视图和缓存的视图
    dispatch('tagsView/delAllViews', null, { root: true })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
