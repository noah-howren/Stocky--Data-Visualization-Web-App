<template>
    <v-app-bar :elevation="24" theme="dark">
        <img :src="image_new" class="img_new"> 
        <div class="search_container" >
            <v-combobox
                    label="Enter a Ticker"
                    :items="tickerList.map(item => item.symbol)"
                    density="comfortable"
                    v-model="selectedTicker"
                    @v-on:keyup.enter="search"
            ></v-combobox>
            <div class="srch_btn_container">
                <v-btn
                    x-large
                    v-on:click="search"
                    color="green"
                    class="text-xs-center"
                    variant="outlined"
                >
                    Search
                </v-btn>
            </div>
        </div>
        <v-spacer></v-spacer>
        <div class="crypto_btn_container">
            <v-btn
                x-large
                v-on:click="stocks"
                color="blue"
                class="text-xs-center"
                variant="flat"
            >
            Crypto
            </v-btn>
        </div>
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
    </v-app-bar>
</template>

<script>
import json from '@/components/tickers.json';
import img_new from '@/assets/logo.png'
import router from '@/router/index.js'
import { VueElement } from 'vue';
import { routerKey } from 'vue-router';
export default{
    data(){
        return{
            tickerList: json,
            image_new:img_new,
            selectedTicker: ''
        }
    },
    methods:{
        search: function (event){
            router.push('/stocks/' + this.selectedTicker, {redirectCode: 301})
        },
        stocks: function (event){
            router.push('/', {redirectCode: 301})
        }
    }
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

.v-combobox {
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