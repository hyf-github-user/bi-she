import Layout from '@/layout'

const permissionRouter = {
  path: '/permissions',
  component: Layout,
  name: '权限管理',
  alwaysShow: true, // 当子路由有一个不显示时会导致这个父路由不显示,可以设置alwayShow属性进行总是显示
  meta: {
    title: '权限管理',
    icon: 'people',
    roles: ['admin']
  },
  children: [
    {
      path: 'ManagePermission',
      component: () => import('@/views/permission'), // 父路由
      name: '管理权限',
      meta: { title: '管理权限', roles: ['admin'], icon: 'list' }
    }
  ]
}
export default permissionRouter
