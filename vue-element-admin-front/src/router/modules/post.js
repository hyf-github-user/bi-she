import Layout from '@/layout'

const postRouter = {
  path: '/posts',
  component: Layout,
  redirect: '/posts/list',
  name: 'posts',
  meta: {
    title: '文章管理',
    icon: 'el-icon-s-help'
  },
  children: [
    {
      path: 'create',
      component: () => import('@/views/posts/create'),
      name: 'CreateArticle',
      meta: { title: '创建文章', icon: 'edit' }
    },
    {
      path: 'edit/:id(\\d+)',
      component: () => import('@/views/posts/edit'),
      name: 'EditArticle',
      meta: { title: '编辑文章', noCache: true, activeMenu: '/posts/list' },
      hidden: true
    },
    {
      path: 'list',
      component: () => import('@/views/posts/list'),
      name: 'ArticleList',
      meta: { title: '文章列表', icon: 'list' }
    }
  ]
}
export default postRouter
