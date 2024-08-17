<template>
        <v-app-bar :elevation="24" theme="dark">
            <img :src="logo" class="logo"> 
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
        <div class="marquee_container">
            <Vue3Marquee
                :key="volumeList.length"
                :loop=0
                :duration = 60
                :clone="false"
                :pauseOnHover="true">
                <div style="display: flex; gap: 50px;"> 
                    <router-link 
                        v-for="item in volumeList" 
                        :key="item.symbol" 
                        :to="item.symbol"
                    >
                    <span class="symbol">
                        {{ item.symbol }}
                    </span>
                    <span v-if="item.change > 0" class="if-up">
                        {{ " " + item.price + " ↑"}}
                    </span>
                    <span v-else class="if-down">
                        {{ " " +  item.price + " ↓" }}
                    </span>
                    </router-link>
                </div>
                <span>     \\\     </span>
            </Vue3Marquee>
        </div>
</template>

<script>
import logo_stocks from '@/assets/logo.png'
import logo_crypto from '@/assets/crypto_logo.png'
import { useRoute } from 'vue-router'
import router from '@/router/index.js'
import axios from 'axios'
export default{

    data(){
        return{
            tickerList: [],
            volumeList: [],
            exchange: "NASDAQ",
            logo:logo_stocks,
            selectedTicker: ''
        }
    },
    methods:{
        
        search: function (event){
            console.log(this.$route.path)
            if (this.$route.path.startsWith('/crypto')) {
                router.push('/crypto/' + this.selectedTicker, {redirectCode: 301})
            }
            else{
                router.push('/stocks/' + this.selectedTicker, {redirectCode: 301})
            }
            this.getData();
        },
        stocks: function (event){
            router.push('/stocks/', {redirectCode: 301})
            this.exchange = "stocks";
            this.logo = logo_stocks;
            this.getData();
            this.$forceUpdate();
        },
        crypto: function (event){
            router.push('/crypto/', {redirectCode: 301})
            this.exchange = "crypto";
            this.logo = logo_crypto;
            this.getData();
            this.$forceUpdate();
        },
        async getData() {
            const path = 'http://127.0.0.1:5000/tickerList/' + this.exchange;
            const res = await axios.get(path)
            this.tickerList = res.data['tickers']; 
            this.volumeList = res.data['volume'];
            console.log(this.volumeList.length)
            console.log(this.tickerList.length)
        },
    },
    created(){
        if (this.$route.path.startsWith('/crypto/')) {
            this.exchange = "crypto";
            this.logo = logo_crypto;
        }
        this.getData();
    },
    computed: {
    }
}
</script>

<style scoped>
.logo{
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
.marquee_container{
    padding-top:80px;
    padding-right:10px;
    padding-bottom: 0px;
    width:20%;
}
.symbol{
    color:white
}
.if-up {
  color: green; 
}

.if-down {
  color: red; 
}

</style>