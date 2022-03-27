import Layout from '@/layout'

const categoryRouter = {
  path: '/categories',
  component: Layout,
  name: '分类管理',
  alwaysShow: true, // 当子路由有一个不显示时会导致这个父路由不显示,可以设置alwayShow属性进行总是显示
  meta: {
    title: '分类管理',
    icon: 'peoples',
    roles: ['admin']
  },
  children: [
    {
      path: 'ManageCategory',
      component: () => import('@/views/category'), // 父路由
      name: '分类管理',
      meta: { title: '分类管理', roles: ['admin'], icon: 'people' }
    }
  ]
}
export default categoryRouter
