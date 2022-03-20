import Layout from '@/layout'

const noticeRouter = {
  path: '/notices',
  component: Layout,
  name: '通知管理',
  alwaysShow: true, // 当子路由有一个不显示时会导致这个父路由不显示,可以设置alwayShow属性进行总是显示
  meta: {
    title: '通知管理',
    icon: 'message',
    roles: ['admin', 'editor']
  },
  children: [
    {
      path: 'ManageNotice',
      component: () => import('@/views/notices/ManageNotice'), // 父路由
      name: '管理通知',
      meta: { title: '管理通知', roles: ['admin', 'editor'], icon: 'message' }
    },
    {
      path: 'PublishNotice',
      name: '发布通知',
      component: () => import('@/views/notices/PublishNotice'),
      meta: { title: '发布通知', roles: ['admin', 'editor'], icon: 'el-icon-circle-plus' }
    }
  ]
}
export default noticeRouter
