import Layout from '@/layout'

const roleRouter = {
  path: '/roles',
  component: Layout,
  name: '角色管理',
  alwaysShow: true, // 当子路由有一个不显示时会导致这个父路由不显示,可以设置alwayShow属性进行总是显示
  meta: {
    title: '角色管理',
    icon: 'user',
    roles: ['admin']
  },
  children: [
    {
      path: 'ManageRole',
      component: () => import('@/views/role'), // 父路由
      name: '管理角色',
      meta: { title: '角色管理', roles: ['admin'], icon: 'list' }
    }
  ]
}
export default roleRouter
