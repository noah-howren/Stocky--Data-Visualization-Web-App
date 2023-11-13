<template>
    <div class="whole_container">
        <div class="logo_container">
            <img :src="image">
        </div>
            <div class="search_container">
                <v-col cols="12">
                    <v-combobox
                        label="Ticker"
                        :items="tickerList.map(item => item.symbol)"
                        density="comfortable"
                        v-model="selectedTicker"
                    ></v-combobox>
                <v-btn
                    v-on:click="search"
                    color="green">
                    Search
                </v-btn>
                </v-col>
            </div>
    </div>
</template>
, VueApexCharts
<script>
import json from '@/components/tickers.json';
import img from '@/assets/stocky_logo.png'
import router from '@/router/index.js'
import { VueElement } from 'vue';
import { routerKey } from 'vue-router';
export default{
data(){
    return{
        tickerList: json,
        image:img,
        selectedTicker: ''
    }
},
methods:{
    search: function (event){
        alert('Selected Ticker: ' + this.selectedTicker);
        router.push('/stocks/' + this.selectedTicker, {redirectCode: 301})
    }
}
}
</script>
<style>
.logo_container{
    transform: scale(.25);
    transform-origin: left;
    padding-top:0px;
    padding-left:0px;
    padding-bottom:0px;
    padding-right:0px;
}
.search_container {
    display: flex;
    width: 100vh;
    height: 100vh; 
    padding-top:0px;
    padding-left:0px;
    padding-bottom:0px;
    padding-right:0px;
}
</style>