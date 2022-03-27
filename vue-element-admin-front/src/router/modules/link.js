import Layout from '@/layout'

const linkRouter = {
  path: '/links',
  component: Layout,
  name: '链接管理',
  alwaysShow: true, // 当子路由有一个不显示时会导致这个父路由不显示,可以设置alwayShow属性进行总是显示
  meta: {
    title: '链接管理',
    icon: 'peoples',
    roles: ['admin']
  },
  children: [
    {
      path: 'ManageLink',
      component: () => import('@/views/link'), // 父路由
      name: '链接管理',
      meta: { title: '链接管理', roles: ['admin'], icon: 'people' }
    }
  ]
}
export default linkRouter
