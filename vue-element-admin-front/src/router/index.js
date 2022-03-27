import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/* 侧边栏的路由 */
// 组件侧边栏
import componentsRouter from './modules/components'
// 用户管理侧边栏
import userRouter from './modules/users'
import postRouter from '@/router/modules/post'
import commentRouter from '@/router/modules/comment'
import categoryRouter from '@/router/modules/category'
import linkRouter from '@/router/modules/link'
// 导入通知路由
import noticeRouter from './modules/notifications'
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
  userRouter, // 用户管理
  postRouter, // 文章管理
  commentRouter, // 评论管理
  categoryRouter, // 分类管理
  linkRouter, // 链接管理
  noticeRouter, // 通知路由
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
  componentsRouter,
  // 后台系统工具
  {
    path: '/tool',
    component: Layout,
    redirect: 'noRedirect',
    alwaysShow: true,
    name: 'tool',
    meta: {
      roles: ['admin'],
      title: '系统工具',
      icon: 'el-icon-s-tools'
    },
    children: [
      {
        path: 'management',
        component: () => import('@/views/tool/backend_manage'),
        name: 'tool-manage',
        meta: { roles: ['admin'], title: '后台管理', icon: 'el-icon-s-operation', noCache: true }
      },
      {
        path: 'swagger',
        component: () => import('@/views/tool/swagger'),
        name: 'tool-swagger',
        meta: { roles: ['admin'], title: '系统接口', icon: 'documentation', noCache: true }
      }
    ]
  },
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
