import Layout from '@/layout'

const linkRouter = {
  path: '/notices',
  component: Layout,
  name: '通知管理',
  alwaysShow: true, // 当子路由有一个不显示时会导致这个父路由不显示,可以设置alwayShow属性进行总是显示
  meta: {
    title: '通知管理',
    icon: 'link',
    roles: ['admin', 'editor']
  },
  children: [
    {
      path: 'ManageNotification',
      component: () => import('@/views/notices'), // 父路由
      name: '管理通知',
      meta: { title: '管理通知', icon: 'list' }
    }
  ]
}
export default linkRouter
