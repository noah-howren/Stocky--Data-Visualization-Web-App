<template>
    <v-app-bar :elevation="24" theme="dark">
        <img :src="image_new" class="img_new"> 
        <div class="search_container" >
            <v-combobox
                label="Enter a Stock Ticker"
                :items="tickerList"
                density="comfortable"
                v-model="selectedTicker"
                class="stocks"
            ></v-combobox>
            <div class="srch_btn_container">
                <v-btn
                    x-large
                    v-on:click="search"
                    color="green"
                    class="text-xs-center"
                    variant="flat"
                >
                    Search
                </v-btn>
            </div>
        </div>
        <v-spacer></v-spacer>
        <div class="stocks_btn_container">
            <v-btn
                x-large
                v-on:click="stocks"
                color="green"
                class="text-xs-center"
                variant="flat"
            >
                Stocks
            </v-btn>
        </div>
        <div class="crypto_btn_container">
            <v-btn
                x-large
                v-on:click="crypto"
                color="deep-purple-accent-2"
                class="text-xs-center"
                variant="flat"
            >
            Crypto
            </v-btn>
        </div>
    </v-app-bar>
</template>

<script>
import img_new from '@/assets/logo.png'
import router from '@/router/index.js'
import axios from 'axios'
import { VueElement } from 'vue';
import { routerKey } from 'vue-router';
export default{
    data(){
        return{
            tickerList: [],
            image_new:img_new,
            selectedTicker: ''
        }
    },
    methods:{
        
        search: function (event){
            router.push('/stocks/' + this.selectedTicker, {redirectCode: 301})
        },
        stocks: function (event){
            router.push('/stocks/', {redirectCode: 301})
        },
        crypto: function (event){
            router.push('/crypto/', {redirectCode: 301})
        },
        async getData() {
            console.log('hi')
            const path = 'http://127.0.0.1:5000/tickerList/NASDAQ';
            const res = await axios.get(path)
            this.tickerList = res.data; 
        },
    },
    created(){
        this.getData();
    },
}
</script>

<style scoped>
.img_new{
    margin-left: 20px;
}
.search_container {
    display:flex;
    flex-direction: row;
    margin-left: 20px; 
    padding-top:20px;/* Adjust the margin as needed */
}
.exchanges{
    width:150px;
    margin-right:10px;
}
.stocks {
    width: 300px; 
    margin-right: 20px;
}
.srch_btn_container{
    margin-top:10px; 
}
.crypto_btn_container{
    margin-left:10px;
    margin-right:10px; 
}
.stocks_btn_container{
    margin-left:10px;
    margin-right:20px; 
}
</style>