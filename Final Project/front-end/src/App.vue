<!-- Use preprocessors via the lang attribute! e.g. <template lang="pug"> -->
<template>
  <div id="app">
    <h1>NLP Final Project</h1>
    <input type="text" v-model="query" name="msg">
    <button v-on:click="Search_handler">Search</button>
    <p v-if="Search_Status"></p>
    <p v-else>搜尋失敗，請再試一次!</p>
    <ul>
      <!--eslint-disable-next-line-->
      <li v-for="(val, key) in Search_result" style="text-align:left;font-size: 30px;color: red">
        {{key}}
        <div v-for="(vv,kk) in val" :key="kk" style="text-align:left;font-size: 18px;color: black">
          <p>{{kk}}:{{vv}}</p>
        </div>
      </li>
    </ul>

  </div>
</template>

<script>
  import axios from "axios";

  export default {
    data() {
      return {
        query: '',
        Search_result: {},
        Search_Status: true,
        requestText:""
      };
    },
    methods: {
      Search_handler() {
        alert(`欲查詢英文詞彙: ${this.query}`)

        axios.get('/here/js_get',{
            params:{
              query:this.query,
            }
          }).then((res)=>{
            //res.data就是http請求返回的資料，我們獲取後可用作資料展示
            this.Search_result = res.data;
            //this.Search_result = {'Status': 'success'};
          },(err)=>{
            //請求失敗時進入這部分；比如500，404等情況

            err = {'Prefix': {'功能1':123, '功能2':456,'功能3':789}, 'Affix': {'功能1':111, '功能2':"222", '功能3':333}};
            //err = ""
            this.Search_result = err;
            this.$data.Search_Status = false
          })
        this.$data.query = ''
      }
    }
  };
</script>

<!-- Use preprocessors via the lang attribute! e.g. <style lang="scss"> -->
<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

  a,
  button {
    color: #4fc08d;
  }

  button {
    background: none;
    border: solid 1px;
    border-radius: 2em;
    font: inherit;
    padding: 0.75em 2em;
  }
</style>

