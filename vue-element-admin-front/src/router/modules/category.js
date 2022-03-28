import Layout from '@/layout'

const categoryRouter = {
  path: '/categories',
  component: Layout,
  name: '分类管理',
  alwaysShow: true, // 当子路由有一个不显示时会导致这个父路由不显示,可以设置alwayShow属性进行总是显示
  meta: {
    title: '分类管理',
    icon: 'nested',
    roles: ['admin', 'editor']
  },
  children: [
    {
      path: 'ManageCategory',
      component: () => import('@/views/category'), // 父路由
      name: '管理分类',
      meta: { title: '管理分类', icon: 'list' }
    }
  ]
}
export default categoryRouter
