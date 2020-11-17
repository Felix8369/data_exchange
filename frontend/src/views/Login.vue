<template>
<div class="login">
  <div class="card">
    <a-form
      id="components-form-demo-normal-login"
      :form="form"
      class="login-form"
      @submit="handleSubmit"
    >
      <div class="input-bg">
      <a-form-item>
        <a-input
          v-decorator="[
            'userName',
            { rules: [{ required: true, message: 'Please input your username!' }] },
          ]"
          placeholder="Username"
        >
          <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)" />
        </a-input>
      </a-form-item>
      </div>
      <div class="input-bg">
      <a-form-item>
        <a-input
          v-decorator="[
            'password',
            { rules: [{ required: true, message: 'Please input your Password!' }] },
          ]"
          type="password"
          placeholder="Password"
        >
          <a-icon slot="prefix" type="lock" style="color: rgba(0,0,0,.25)" />
        </a-input>
      </a-form-item>
      </div>
      <a-form-item>
        <!-- <a-checkbox
          v-decorator="[
            'remember',
            {
              valuePropName: 'checked',
              initialValue: true,
            },
          ]"
        >
          Remember me
        </a-checkbox> -->
        <a class="login-form-forgot" href="">
          Forgot password
        </a>
        <a-button type="primary" html-type="submit" class="login-form-button">
          Log in
        </a-button>
        <!-- Or
        <a href="">
          register now!
        </a> -->
      </a-form-item>
    </a-form>
  </div>
</div>
</template>

<script>
export default {
  created() {
    // this.getImage();
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: 'normal_login' });
  },
  data() {
    return {
      rootPath: "",
      img: "",
      uuid_n: "",
      code: "",
      err_status: "success",
      err_help: "",
      pubKey: "",
      loginLoading: false,
      imgurl: "",
      uuid: ""
    };
  },
  methods: {
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFields((err, values) => {
        if (!err) {
          this.loginLoading = true;
          this.$axios({
            method: "post",
            url: this.$eg.API.login,
            data: {
              username: values.userName,
              password: values.password,
              content: values.code,
              uuid: this.uuid
            }
          })
            .then(res => {
              this.loginLoading = false;
              if (res.data.errCode === this.$eg.SUCCESS) {
                this.err_status = "success";
                this.err_help = "";
                let obj = res.data.data;
                this.$eg.setStorage("baseMessage", obj);

                // 跳转到首页
                let name = "Index";
                this.$router.push({ name: name });
              } else {
                // 提示信息设置
                this.err_status = "error";
                this.err_help = res.data.errMsg;
              }
              // this.getImage();
            })
            .catch(err => {
              console.log(err);
              this.loginLoading = false;
              // this.getImage();
            });
        }
      });
    },
    getImage() {
      this.$axios({
        method: "get",
        url: "/api/captcha",
        responseType: "blob"
      }).then(res => {
        let blobUrl = window.URL.createObjectURL(res.data);
        this.imgurl = blobUrl;
        this.uuid = res.headers.uuid;
        // 不能清理
        // window.URL.revokeObjectURL(blobUrl);
        console.log(res);
      });
    }
  },
};
</script>

<style lang="less">
.login{
  width:100%;
  height: 100vh;
  background: url("/img/bodybg.jpg");
  background-size: 100% 100%;
  padding-top: 400px;
  .card{
    margin-left: 200px;
    .login-form {
      padding-top: 60px;
      margin-right: 180px;
      width: 440px;

    }  
  }
}

#components-form-demo-normal-login .login-form {
  max-width: 300px;
}
#components-form-demo-normal-login .login-form-forgot {
  float: right;
}
#components-form-demo-normal-login .login-form-button {
  width: 100%;
}
</style>