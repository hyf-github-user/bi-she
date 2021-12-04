import Layout from '@/layout'

const userRouter = {
  path: '/user',
  component: Layout,
  name: '用户管理',
  meta: {
    title: '用户管理',
    icon: 'nested'
  },
  children: [
    {
      path: 'ManageUser',
      component: () => import('@/views/user/ManageUser/index'), // 父路由
      name: '管理用户',
      meta: { title: '管理用户' }
    },
    {
      path: 'AddUser',
      name: '添加用户',
      component: () => import('@/views/user/AddUser/index'),
      meta: { title: '添加用户' }
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
