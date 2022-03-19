import Layout from '@/layout'

const articleRouter = {
  path: '/article',
  component: Layout,
  name: '文章管理',
  alwaysShow: true, // 当子路由有一个不显示时会导致这个父路由不显示,可以设置alwayShow属性进行总是显示
  meta: {
    title: '文章管理',
    icon: 'example',
    roles: ['admin', 'editor']
  },
  children: [
    {
      path: 'ManageArticles',
      component: () => import('@/views/blog/components/posts/ManageArticles'), // 父路由
      name: '管理文章',
      meta: { title: '管理文章', roles: ['admin', 'editor'], icon: 'list' }
    },
    {
      path: 'AddArticle',
      name: '创建文章',
      component: () => import('@/views/blog/components/posts/AddArticle'),
      meta: { title: '创建文章', roles: ['admin', 'editor'], icon: 'el-icon-circle-plus' }
    }
  ]
}
export default articleRouter
