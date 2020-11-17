
const SECRET_KEY = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
const SUCCESS = '00000000';
const ERROR = '00001001'; // 系统错误
const TOKEN_LOST = '00001002'; // token缺少
const TOKEN_ERROR = '00001003'; // token 错误

const API = {
    login: '/v1/login', // post 
    logout: '/v1/logout', // post
}

export default {
    SECRET_KEY,
    SUCCESS,
    TOKEN_LOST,
    TOKEN_ERROR,
    ERROR,
    API
  };