import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    redirect: "/login"
  },
  {
    path: "/home",
    name: "Home",
    meta: {title: "home"},
    component: Home
  },
  {
    path: "/index",
    name: "Index",
    meta: {title: "index"},
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/Index.vue")
  },
  {
    path: "/login",
    name: "Login",
    meta: {title: "login"},
    component: () =>
      import(/* webpackChunkName: "Login" */ "../views/Login.vue")
  },
  {
    path: "/test",
    name: "Test",
    meta: {title: "test"},
    component: () =>
      import(/* webpackChunkName: "Login" */ "../views/Test.vue")
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
