import Layout from '@/layout'

const userRouter = {
  path: '/users',
  component: Layout,
  name: '用户管理',
  alwaysShow: true, // 当子路由有一个不显示时会导致这个父路由不显示,可以设置alwayShow属性进行总是显示
  meta: {
    title: '用户管理',
    icon: 'peoples',
    roles: ['admin', 'editor']
  },
  children: [
    {
      path: 'ManageUser',
      component: () => import('@/views/users'), // 父路由
      name: '管理用户',
      meta: { title: '管理用户', roles: ['admin', 'editor'], icon: 'people' }
    }
  ]
}
export default userRouter
