import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		user: sessionStorage.getItem('user') ? JSON.parse(sessionStorage.getItem('user')) : {},
		userinfo: sessionStorage.getItem('userinfo') ? JSON.parse(sessionStorage.getItem('userinfo')) : {},
		attendances: sessionStorage.getItem('attend') ? JSON.parse(sessionStorage.getItem('attend')) : [],
		Authorization: sessionStorage.getItem('Authorization') ? sessionStorage.getItem('Authorization') : '',
		isLoggedIn: sessionStorage.getItem('isLoggedIn') ? sessionStorage.getItem('isLoggedIn') === 'true' : false // 假设存储的是字符串形式的布尔值
	},
	mutations: {
		setUser(state, value) {
			state.user = value;
			sessionStorage.setItem("user", JSON.stringify(value));
		},
		setUserinfo(state, value) {
			state.userinfo = value;
			sessionStorage.setItem("userinfo", JSON.stringify(value));
		},
		setAttend(state, attendances) {
			attendances.forEach(({ user, competition }) => {
				const existingAttendance = state.attendances.find(attendance =>
					attendance.user === user && attendance.competition === competition
				);

				if (!existingAttendance) {
					// 如果不存在，添加新的出席记录    
					state.attendances.push({ user, competition });
				}
			});
			// 更新 sessionStorage，注意这应该在循环之后执行一次  
			sessionStorage.setItem('attend', JSON.stringify(state.attendances));
		},
		setAuthorization(state, value) {
			state.Authorization = value;
			sessionStorage.setItem("Authorization", value);
		},
		setIsLoggedIn(state, value) {
			state.isLoggedIn = value;
			sessionStorage.setItem("isLoggedIn", value.toString()); // 存储为字符串形式的布尔值  
		}
	},
	actions: {
	},
	modules: {
	}
})
