import Vue from "vue"
import CONFIG from "./config"
import JSEncrypt from 'jsencrypt';
import CryptoJS from 'crypto-js';

function Eg (){
    Object.assign(this, CONFIG)
}

const $eg = new Eg()

Vue.prototype.$eg = $eg

function add(name, func){
    Eg.prototype[name] = func
}

// 设置storage 加密
add('setStorage', function (key, value) {
    if (typeof value !== 'string') {
      value = JSON.stringify(value);
    }
    value = this.decodeData(value);
    sessionStorage.setItem(key, value);
  });
  
  // 获取storage 解密
  add('getStorage', function (key) {
    var value = sessionStorage.getItem(key);
    if (!value) {
      return null;
    }
    return this.encodeData(value);
  });

// 加密  JSEncrypt 密码提交
add('encrypt', function (pubkey, value) {
  var encrypt = new JSEncrypt();
  encrypt.setPublicKey(pubkey);
  return encrypt.encrypt(value);
});

// 加密
add('getAesString', function (data, key, iv) {
  key = CryptoJS.enc.Utf8.parse(key);
  iv = CryptoJS.enc.Utf8.parse(iv);
  var encrypted = CryptoJS.AES.encrypt(data, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  });
  return encrypted.toString(); // 返回的是base64格式的密文
});

// 解密
add('getDAesString', function (encrypted, key, iv) {
  key = CryptoJS.enc.Utf8.parse(key);
  iv = CryptoJS.enc.Utf8.parse(iv);
  var decrypted = CryptoJS.AES.decrypt(encrypted, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  });
  return decrypted.toString(CryptoJS.enc.Utf8);
});

// 本地信息加密函数
add('decodeData', function (data) {
  var key = CONFIG.SECRET_KEY; // 密钥
  var iv = '1234567812345678';
  var encrypted = this.getAesString(data, key, iv); // 密文
  // var encrypted1 = CryptoJS.enc.Utf8.parse(encrypted);
  return encrypted;
});

// 本地信息解密函数
add('encodeData', function (data) {
  var key = CONFIG.SECRET_KEY; // 密钥
  var iv = '1234567812345678';
  var decryptedStr = this.getDAesString(data, key, iv);
  return decryptedStr;
});

// 显示表格数据数量信息
add('showTotal', function (total, range) {
  // return `显示第${range[0]}-${range[1]}条记录,总共${total}条记录`;
  return `显示第${range[0]}-${range[1]}条记录,总共${total}条记录`;
});








  export {
    $eg
  }