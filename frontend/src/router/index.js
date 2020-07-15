import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Search from '@/components/Search'
import Description from '@/components/Description'
import Blank from '@/components/Blank'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/search/:words',
      name: 'Search',
      component: Search
    },
    {
      path: '/description',
      name: 'Description',
      component: Description
    },
    {
      path: '/Blank/:words',
      name: 'Blank',
      component: Blank
    }
  ]
})
