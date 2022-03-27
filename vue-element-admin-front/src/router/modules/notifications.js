import Layout from '@/layout'

const noticeRouter = {
  path: '/notices',
  component: Layout,
  redirect: '/notices/list',
  name: 'notices',
  meta: {
    title: '通知管理',
    icon: 'el-icon-s-help'
  },
  children: [
    {
      path: 'create',
      component: () => import('@/views/notices/create'),
      name: 'CreateArticle',
      meta: { title: '创建通知', icon: 'edit' }
    },
    {
      path: 'edit/:id(\\d+)',
      component: () => import('@/views/notices/edit'),
      name: 'EditArticle',
      meta: { title: '编辑通知', noCache: true, activeMenu: '/notices/list' },
      hidden: true
    },
    {
      path: 'list',
      component: () => import('@/views/notices/list'),
      name: 'ArticleList',
      meta: { title: '通知列表', icon: 'list' }
    }
  ]
}
export default noticeRouter
