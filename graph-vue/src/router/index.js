import Vue from "vue";
import VueRouter from "vue-router";

import Login from "@/components/Login";
import App from "@/App";

Vue.use(VueRouter)

export default new VueRouter({
    routes:[
        {
            path:'/',
            name:'Login',
            component: Login,
            meta:{
                keepalive: false
            }
        },
        {
            path:'/App',
            name:'main',
            component: App,
            meta:{
                keepalive: true
            }
        }
    ]
})





