import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

import AuthLayout from '../layouts/AuthLayout.vue'
import AppLayout from '../layouts/AppLayout.vue'
import PlayLayout from '../layouts/PlayLayout.vue'

import RouteViewComponent from '../layouts/RouterBypass.vue'

import useAuthStore from '@/auth/store'
import { DEFAULT_UNAUTHORIZE_ROUTE } from "@/base/consts"

const routes: Array<RouteRecordRaw> = [
  {
    path: '/:pathMatch(.*)*',
    redirect: { name: 'dashboard' },
  },
  {
    name: 'admin',
    path: '/',
    component: AppLayout,
    redirect: { name: 'dashboard' },
    children: [
      {
        name: 'dashboard',
        path: 'dashboard',
        component: () => import('../pages/admin/dashboard/Dashboard.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        name: 'games',
        path: 'games',
        component: () => import('@/games/pages/Games.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        name: 'questions',
        path: 'games/:gameId/questions',
        component: () => import('@/questions/pages/QuestionList.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        name: 'plays',
        path: 'games/:gameId/plays',
        component: () => import('@/plays/pages/PlayList.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        name: 'playDashboard',
        path: '/playdashboard/:playId',
        component: () => import("@/plays/pages/PlayDashboard.vue"),
        meta: {
          requiresAuth: true
        }
      },
      {
        name: 'settings',
        path: 'settings',
        component: () => import('../pages/settings/Settings.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        name: 'preferences',
        path: 'preferences',
        component: () => import('../pages/preferences/Preferences.vue'),
        meta: {
          requiresAuth: true
        }
      },
      // {
      //   name: 'users',
      //   path: 'users',
      //   component: () => import('../pages/users/UsersPage.vue'),
      // },
      // {
      //   name: 'projects',
      //   path: 'projects',
      //   component: () => import('../pages/projects/ProjectsPage.vue'),
      // },
      // {
      //   name: 'payments',
      //   path: '/payments',
      //   component: RouteViewComponent,
      //   children: [
      //     {
      //       name: 'payment-methods',
      //       path: 'payment-methods',
      //       component: () => import('../pages/payments/PaymentsPage.vue'),
      //     },
      //     {
      //       name: 'billing',
      //       path: 'billing',
      //       component: () => import('../pages/billing/BillingPage.vue'),
      //     },
      //     {
      //       name: 'pricing-plans',
      //       path: 'pricing-plans',
      //       component: () => import('../pages/pricing-plans/PricingPlans.vue'),
      //     },
      //   ],
      // },
      // {
      //   name: 'faq',
      //   path: '/faq',
      //   component: () => import('../pages/faq/FaqPage.vue'),
      // },
    ],
  },
  {
    name: 'playPages',
    path: '/play/:playId',
    component: PlayLayout,
    redirect: { name: 'intro' },
    children: [
      {
        name: 'intro',
        path: '',
        component: () => import('@/plays/pages/intro.vue'),
      },
    ]
  },
  {
    path: '/auth',
    component: AuthLayout,
    children: [
      {
        name: 'login',
        path: 'login',
        component: () => import('@/auth/pages/Login.vue'),
        meta: {
          requiresNoAuth: true
        },
      },
      {
        name: 'logout',
        path: 'logout',
        component: () => import('@/auth/pages/Logout.vue'),
        meta: {
          requiresAuth: true
        },
      },
      {
        name: 'signup',
        path: 'signup',
        component: () => import('../pages/auth/Signup.vue'),
        meta: {
          requiresNoAuth: true
        },
      },
      {
        name: 'recover-password',
        path: 'recover-password',
        component: () => import('../pages/auth/RecoverPassword.vue'),
        meta: {
          requiresNoAuth: true
        },
      },
      {
        name: 'recover-password-email',
        path: 'recover-password-email',
        component: () => import('../pages/auth/CheckTheEmail.vue'),
        meta: {
          requiresNoAuth: true
        },
      },
      {
        path: '',
        redirect: { name: 'login' },
      },
    ],
  },
  {
    name: '404',
    path: '/404',
    component: () => import('../pages/404.vue'),
  },
]


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    // For some reason using documentation example doesn't scroll on page navigation.
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    } else {
      window.scrollTo(0, 0)
    }
  },
  routes,
})
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth) {
    if (authStore.isAuthorized) {
      // User is authenticated, proceed to the route
      next();
    } else {
      // User is not authenticated, redirect to login
      next(DEFAULT_UNAUTHORIZE_ROUTE);
    }
  } else if (to.meta.requiresNoAuth) {
    if (authStore.isAuthorized) {
      // User is authenticated, proceed to the route
      next('/dashboard');
    } else {
      // User is not authenticated, redirect to login
      next();
    }

  } else {
    // Non-protected route, allow access
    next();
  }
})

export default router
