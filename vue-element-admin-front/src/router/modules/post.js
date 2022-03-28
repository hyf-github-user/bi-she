import Layout from '@/layout'

const postRouter = {
  path: '/posts',
  component: Layout,
  redirect: '/posts/list',
  name: 'posts',
  meta: {
    title: '文章管理',
    icon: 'el-icon-s-help',
    roles: ['admin', 'editor']
  },
  children: [
    {
      path: 'create',
      component: () => import('@/views/posts/create'),
      name: '创建文章',
      meta: { title: '创建文章', icon: 'edit' }
    },
    {
      path: 'edit/:id(\\d+)',
      component: () => import('@/views/posts/edit'),
      name: '编辑文章',
      meta: { title: '编辑文章', noCache: true, activeMenu: '/posts/list' },
      hidden: true
    },
    {
      path: 'list',
      component: () => import('@/views/posts/list'),
      name: '管理文章',
      meta: { title: '文章列表', icon: 'list' }
    }
  ]
}
export default postRouter
