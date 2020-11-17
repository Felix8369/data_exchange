import Vue from 'vue';
import moment from 'moment'

  // 过滤时间   format  2019-10-10 10:10:10
Vue.filter("getTime", function(value) {
  if (!value || value < 1) {
    return "-"
  } else {
    let d = new Date(value * 1000);
    let year = d.getFullYear();
    // 补0操作
    let month = d.getMonth() + 1;
    let date = d.getDate();
    let hour = d.getHours();
    let minute = d.getMinutes();
    let second = d.getSeconds();
    month = month < 10 ? "0" + month : month;
    date = date < 10 ? "0" + date : date;
    hour = hour < 10 ? "0" + hour : hour;
    minute = minute < 10 ? "0" + minute : minute;
    second = second < 10 ? "0" + second : second;
    return year + "-" + month + "-" + date + " " + hour + ":" + minute + ':' + second;
  }
});

// 过滤时间   format  10天10时10分
Vue.filter("getTime_b", function(value) {
  value = value * 60;
  if (value < 1 || !value) {
    return "-";
  }
  let daySecond = 24 * 60 * 60;
  let day = parseInt(value / daySecond); // 得到天数
  let cha = value % daySecond;
  let hours = parseInt(cha / 60 / 60); // 小时
  let hcha = cha % (60 * 60);
  let minute = parseInt(hcha / 60); // 分钟
  day = day < 10 ? '0' + day : day;
  hours = hours < 10 ? '0' + hours : hours;
  minute = minute < 10 ? '0' + minute : minute;
  if (day > 0) {
    return day + ' 天 ' + hours + ' 时 ' + minute + ' 分';
  } else {
    return hours + ' 时 ' + minute + ' 分';
  }
});

// 过滤时间   format  10:10:10
Vue.filter("getTime_c", function(value) {
  if (value < 1 || !value) {
    return "00 : 00 : 00";
  }
  let hours = parseInt(value / 60 / 60); // 小时
  let hcha = value % (60 * 60);
  let minute = parseInt(hcha / 60); // 分钟
  let second = hcha % 60;

  hours = hours < 10 ? '0' + hours : hours;
  minute = minute < 10 ? '0' + minute : minute;
  second = second < 10 ? '0' + second : second;

  return hours + ' : ' + minute + ' : ' + second;
});

Vue.filter('moment', function(dataStr, pattern = 'YYYY-MM-DD HH:mm:ss') {
  return moment(dataStr * 1000).format(pattern)
});