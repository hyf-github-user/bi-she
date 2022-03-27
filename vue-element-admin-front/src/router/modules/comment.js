import Layout from '@/layout'

const commentRouter = {
  path: '/comments',
  component: Layout,
  name: '评论管理',
  alwaysShow: true, // 当子路由有一个不显示时会导致这个父路由不显示,可以设置alwayShow属性进行总是显示
  meta: {
    title: '评论管理',
    icon: 'message',
    roles: ['admin']
  },
  children: [
    {
      path: 'ManageComment',
      component: () => import('@/views/comments'), // 父路由
      name: '管理评论',
      meta: { title: '管理评论', roles: ['admin'], icon: 'list' }
    }
  ]
}
export default commentRouter
