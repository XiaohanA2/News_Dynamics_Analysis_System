import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  // {
  //   path: '/login',
  //   component: () => import('@/views/login/index'),
  //   hidden: true
  // },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/single-news-fashion/index'
  },

  {
    path: '/single-news-fashion',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'single-news-fashion',
        component: () => import('@/views/a-single-news-fashion/index'),
        meta: { title: '单新闻流行变化', icon: 'nested' }
      }
    ]
  },

  {
    path: '/category-news-changing',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'category-news-changing',
        component: () => import('@/views/b-category-news-changing/index'),
        meta: { title: '某种类新闻变化', icon: 'list' }
      }
    ]
  },

  {
    path: '/user-interest-changing',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'user-interest-changing',
        component: () => import('@/views/c-user-interest-changing/index'),
        meta: { title: '用户兴趣变化', icon: 'star' }
      }
    ]
  },

  {
    path: '/comprehensive-search',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'comprehensive-search',
        component: () => import('@/views/d-comprehensive-search/index'),
        meta: { title: '组合统计查询', icon: 'tree-table' }
      }
    ]
  },

  {
    path: '/dynamic-recommendation',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'dynamic-recommendation',
        component: () => import('@/views/e-dynamic-recommendation/index'),
        meta: { title: '实时推荐', icon: 'example' }
      }
    ]
  },

  {
    path: '/hot',
    component: Layout,
    children: [{
      path: 'index',
      name: 'hot',
      component: () => import('@/views/f-hot-news-suggestion/index'),
      meta: { title: '爆款新闻分析', icon: 'fire' }
    }]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
