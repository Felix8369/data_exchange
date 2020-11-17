import axios from "axios"
import Vue from "vue"
import CONFIG from "./config"
import { $eg } from "./common"

Vue.prototype.$axios = axios

// 设置请求超时时间
axios.defaults.timeout = 60000;

// 返回拦截器
axios.interceptors.response.use(
  response => {
    // console.log(response)
    return Promise.resolve(response)
  }, error => {
    $eg.networkError(error)
  });


// config 配置与官方一致；
function req(config, method, ctype='application/json') {
    let baseMessage = JSON.parse($eg.getStorage('baseMessage'));
    let token = baseMessage != null ? baseMessage.api_token : null;
    return new Promise((resolve, reject) => {
      axios({
          headers: {
            'Api-Token': token,
            'Content-Type': ctype
          },
          ...config,
          method: method
        })
        .then(res => {
          if (res.data.errCode !== CONFIG.SUCCESS) {
            $eg.statusCode(res);
          }
          resolve(res);
        }).catch(err => {
          reject(err)
        })
    })
  }
  
let obj = ["get", "post", "put", "delete", "patch"];
for (let k in obj) {
  let name = k.replace(/\$/, '');
  Vue.prototype['$' + name] = (config, ctype)=>{return req(config, k, ctype)};
}
export default obj;