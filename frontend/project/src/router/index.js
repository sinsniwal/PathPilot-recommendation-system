import { createRouter, createWebHashHistory } from "vue-router";
import Home from "../components/Home.vue"
import Recommend from "../components/Recommend.vue"

const routes = [
    { path: '/', component: Home },
    { path: '/recommend', component: Recommend},
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

export default router