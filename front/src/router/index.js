import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/layout/index.vue'

Vue.use(VueRouter)

const routes = [
	{
		path: '/',
		component: Layout,
		redirect: 'majorPage',
		children: [
			{
				path: '/',
				name: 'majorPage',
				component: () => import('../views/majorPage.vue'),
				meta: {
					title: '首页'
				}
			},
			{
				path: 'exam',
				component: () => import('../views/Exam.vue'),
				name: 'exam',
				meta: {
					title: '场景'
				}
			},
			{
				path: 'competition',
				name: 'Competition',
				component: () => import('../views/Competition.vue'),
				meta: {
					title: '所有比赛'
				}
			},
			{
				path: 'mygame',
				name: 'MyGame',
				component: () => import('../views/MyGame.vue'),
				meta: {
					title: '我的比赛'
				}
			},
			{
				path: 'works',
				name: 'works',
				component: () => import('../views/Works.vue'),
				meta: {
					title: '作品管理'
				}
			},
			{
				path: 'grade',
				name: 'Grade',
				component: () => import('../views/Grade.vue'),
				meta: {
					title: '排行榜'
				}
			},
			{
				path: 'center',
				name: 'Center',
				component: () => import('../views/Center.vue'),
				meta: {
					title: '个人中心'
				}
			},
			{
				path: 'password',
				name: 'Password',
				component: () => import('../views/Password.vue'),
				meta: {
					title: '修改密码'
				}
			},
			{
				path: 'MyCustomWorks',
				name: 'MyCustomWorks',
				component: () => import('../views/MyCustomWorks.vue'),
				meta: {
					title: '自定义场景'
				}
			},
		]
	},
	{
		path: '/login',
		name: 'Login',
		component: () => import('../views/Login.vue'),
		meta: {
			title: '登录界面'
		}
	},
	{
		path: '/register',
		name: 'Register',
		component: () => import('../views/Register.vue'),
		meta: {
			title: '注册界面'
		}
	},
]

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes
})

// 导航守卫
// 使用 router.beforeEach 注册一个全局前置守卫，判断用户是否登陆
// router.beforeEach((to, from, next) => {
// 	设置标题
// 	if (to.meta.title) {
// 		document.title = to.meta.title
// 	}

// 	if (to.path === '/login' || to.path === '/register') {
// 		next();
// 	} else {
// 		let token = sessionStorage.getItem('Authorization');
// 		if (token === null || token === '') {
// 			next('/login');
// 		} else {
// 			next();
// 		}
// 	}

// });
export default router
