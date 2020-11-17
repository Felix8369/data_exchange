<template>
  <div id="app">
    <!-- <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/index">About</router-link> |
      <router-link to="/login">Login</router-link> |
      <router-link to="/test">Test</router-link> 
    </div> -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: "app",
  created(){
    this.baseMessage = JSON.parse(this.$eg.getStorage("baseMessage"));
  },
  data(){
    return {
      titleText:"",
    }
  },
  watch: {
    $route() {
      this.setTitle();
    }
  },
  methods:{
    getLocal() {
      let lang = this.$eg.getStorage("lang");
      this.locale = this.$i18n.getLocaleMessage(lang).antLocale || this.zh_CN;
      this.setTitle();
    },
    setTitle() {
      // setTimeout解决刷新页面时title默认显示中文问题
      setTimeout(() => {
        this.titleText = this.$route.meta.title;
        document.title = this.titleText ? this.titleText + " - " + "数据平台" : "数据平台";
      });
    },

  },

}

</script>

<style lang="less">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
