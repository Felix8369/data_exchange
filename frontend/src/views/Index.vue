<template>
  <div class="about">
    <h1>This is an Index page</h1>
    <div class="logout">
      <a-button type="primary" @click="logout">
        退出登陆
      </a-button>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return {

    }
  },
  methods: {
    logout(){
      this.$eg.setStorage("baseMessage", {});
      this.$router.push({ name: "Login" });
    }
  }
  
}
</script>

<style lang="less" scoped>
.logout{
  position: absolute;
  top: 100px;
  right: 10px;
}
</style>

