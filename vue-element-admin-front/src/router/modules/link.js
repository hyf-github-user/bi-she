import Layout from '@/layout'

const linkRouter = {
  path: '/links',
  component: Layout,
  name: '链接管理',
  alwaysShow: true, // 当子路由有一个不显示时会导致这个父路由不显示,可以设置alwayShow属性进行总是显示
  meta: {
    title: '链接管理',
    icon: 'link',
    roles: ['admin', 'editor']
  },
  children: [
    {
      path: 'ManageLink',
      component: () => import('@/views/link'), // 父路由
      name: '管理链接',
      meta: { title: '链接管理', icon: 'list' }
    }
  ]
}
export default linkRouter
