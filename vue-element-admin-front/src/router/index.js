import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/* 侧边栏的路由 */
// 组件侧边栏
import componentsRouter from './modules/components'
// 图标侧边栏
import chartsRouter from './modules/charts'
// table侧边栏
import tableRouter from './modules/table'
// 用户管理侧边栏
import userRouter from './modules/users'
// 导入通知路由
// import noticeRouter from './modules/notifications'
// // 导入文章路由
// import articleRouter from './modules/post'
// 固定的路由
export const constantRoutes = [
  // 下面都是登录的路由
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  // 登录成功展示的页面
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index'),
        name: 'Dashboard',
        meta: { title: '博客管理系统', icon: 'dashboard', affix: true }
      }
    ]
  },
  // 展示图标
  {
    path: '/icon',
    component: Layout,
    children: [
      {
        path: 'index',
        component: () => import('@/views/icons/index'),
        name: 'Icons',
        meta: { title: '图标', icon: 'icon', noCache: true }
      }
    ]
  },
  // 个人中心的路由
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    hidden: true,
    children: [
      {
        path: 'index',
        component: () => import('@/views/profile/index'),
        name: 'Profile',
        meta: { title: '个人中心', icon: 'user', noCache: true }
      }
    ]
  }
]

// 根据用户的身份多态加载的路由
export const asyncRoutes = [
  // 权限的路由
  {
    path: '/permission',
    component: Layout,
    redirect: '/permission/page',
    alwaysShow: true, // will always show the root menu
    name: 'Permission',
    meta: {
      title: '权限测试页',
      icon: 'lock',
      roles: ['editor', 'admin'] // you can set roles in root nav
    },
    children: [
      {
        path: 'page',
        component: () => import('@/views/permission/page'),
        name: 'PagePermission',
        meta: {
          title: '页面权限',
          roles: ['admin', 'editor'] // or you can only set roles in sub nav
        }
      },
      {
        path: 'directive',
        component: () => import('@/views/permission/directive'),
        name: 'DirectivePermission',
        meta: {
          title: '指令权限'
          // if do not set roles, means: this page does not require permission
        }
      },
      {
        path: 'role',
        component: () => import('@/views/permission/role'),
        name: 'RolePermission',
        meta: {
          title: '角色权限',
          roles: ['admin']
        }
      }
    ]
  },
  /** 当你的路由太长了,可以采用模块化的方法 **/
  // 示例路由
  {
    path: '/example',
    component: Layout,
    redirect: '/example/list',
    name: 'Example',
    meta: {
      title: '综合实例',
      icon: 'el-icon-s-help'
    },
    children: [
      {
        path: 'create',
        component: () => import('@/views/example/create'),
        name: 'CreateArticle',
        meta: { title: '创建文章', icon: 'edit' }
      },
      {
        path: 'edit/:id(\\d+)',
        component: () => import('@/views/example/edit'),
        name: 'EditArticle',
        meta: { title: '编辑文章', noCache: true, activeMenu: '/example/list' },
        hidden: true
      },
      {
        path: 'list',
        component: () => import('@/views/example/list'),
        name: 'ArticleList',
        meta: { title: '文章列表', icon: 'list' }
      }
    ]
  },
  userRouter, // 用户管理
  // noticeRouter, // 通知路由
  // articleRouter, // 文章路由
  // 系统监控
  {
    path: '/monitor',
    component: Layout,
    redirect: 'noRedirect',
    alwaysShow: true,
    name: 'monitor',
    meta: {
      title: '系统监控',
      icon: 'el-icon-data-analysis',
      roles: ['admin']
    },
    children: [
      {
        path: 'users',
        component: () => import('@/views/monitor/users'),
        name: 'monitor-users',
        meta: { title: '在线用户', icon: 'people', roles: ['admin'], noCache: true }
      },
      {
        path: 'ip',
        component: () => import('@/views/monitor/ip'),
        name: 'monitor-ip',
        meta: { title: 'IP黑名单', icon: 'eye', roles: ['admin'], noCache: true }
      },
      {
        path: 'service',
        component: () => import('@/views/monitor/service'),
        name: 'monitor-service',
        meta: { title: '服务监控', icon: 'el-icon-s-home', roles: ['admin'], noCache: true }
      }
    ]
  },
  // 表格的路由
  {
    path: '/tab',
    component: Layout,
    children: [
      {
        path: 'index',
        component: () => import('@/views/tab/index'),
        name: 'Tab',
        meta: { title: 'Tab', icon: 'tab' }
      }
    ]
  },
  componentsRouter,
  chartsRouter,
  tableRouter,
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // 去除URL带有的#号
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
