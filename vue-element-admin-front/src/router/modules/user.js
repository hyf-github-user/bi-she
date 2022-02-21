import Layout from '@/layout'

const userRouter = {
  path: '/user',
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
      component: () => import('@/views/user/ManageUser/index'), // 父路由
      name: '管理用户',
      meta: { title: '管理用户', roles: ['admin', 'editor'], icon: 'people' }
    },
    {
      path: 'AddUser',
      name: '添加用户',
      component: () => import('@/views/user/AddUser/index'),
      meta: { title: '添加用户', roles: ['admin'], icon: 'el-icon-circle-plus' }
    },
    {
      path: 'UpdateUser',
      name: '更新用户',
      component: () => import('@/views/user/UpdateUser/index'),
      meta: { title: '更新用户' },
      hidden: true // 隐藏这个菜单栏
    }
  ]
}
export default userRouter
