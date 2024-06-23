<template>
    <v-app app theme="myCustomDark" >
        <div class="whole_container">
                <nav_bar></nav_bar>
            <div class="button_container">
                <v-btn-toggle
                    v-model="text"
                    rounded="10"
                    color="green-accent-4"
                    divided
                    @update="refreshPage"
                >
                    <v-btn value="d">
                        Daily
                    </v-btn>
                    <v-btn value="w">
                        Weekly
                    </v-btn>
                    <v-btn value="m">
                        Monthly
                    </v-btn>
                    <v-btn value="y">
                        Yearly
                    </v-btn>
                </v-btn-toggle>
            </div>
            <div class="chart_container">
                <apexchart 
                    type="candlestick"
                    height="600"
                    width="1200"
                    :series="series"
                    :options="chartOptions"
                />
            </div>
            <div class="news_container" style="display: inline">
                Latest News:
                <li v-for="(article, index) in newslst">
                    <v-img :src=article.image_url
                        height="400px"
                        width="400px">
                    </v-img>
                    <a :href="article.url" target=article.url> {{article.title}}</a>
                </li>
            </div>
        </div>
    </v-app>
</template>

<script>
import img from '@/assets/stocky_logo.png';
import axios from 'axios';
import ApexCharts from 'vue3-apexcharts';
import nav_bar from '@/components/nav_bar/nav_bar.vue';
export default{
    mounted(){
        document.title = "Stocky | " + this.$route.params.Ticker;
    },
    components: {
        apexchart: ApexCharts,
        nav_bar
    },
    data(){
        console.log('hello')
        return{
            text: 'd',
            image:img,
            data:[],
            seriesData:[],
            series:[],
            newslst:[],
            tickSON: {'d':'39',
               'w':'21',
               'm':'30',
               'y':'63'},
            chartOptions: {
                chart:{
                    type: 'candlestick',
                    height: 600,
                    width: 1200,
                    id: 'candles'
                },
                zoom: {
                    enabled: false
                },
                title:{ 
                    text:this.$route.params.Ticker,
                    align:'left',
                    style: {
                        color: 'white',
                        fontSize:  '16px',
                        fontWeight:  'bold'
                    },
                },
                tooltip:{
                    enabled: true,
                    followCursor: true,
                    style:{
                        color:'black'
                    }
                },
                yaxis: {
                    forceNiceScale: true,
                    labels:{
                        formatter: function (value) {
                            return '$' + value.toFixed(2); // Display rounded integers only
                        },
                        style:{
                            colors:'white'
                        }
                    },
                },
                xaxis:{
                    tickAmount: 39,
                    labels:{
                        style:{
                            colors:'white'
                        }
                    }
                }
            }
        }
    },
    computed:{
        selectedInterval() {
            return this.text;
        }
    },
    watch: {
        '$route.params':'searchBar',
        selectedInterval(newValue, oldValue) {
            if (newValue !== oldValue) {
                this.refreshPage();
            }
        }
    },
    methods:{
        async getData() {
            //console.log('hi')
            const path = 'http://127.0.0.1:5000/query/stocks/' + this.$route.params.Ticker + '/' +this.selectedInterval;
            const res = await axios.get(path)
            if(!res.code){
                this.seriesData = Object.entries(res.data).map(([key, value]) => ({
                    x: value['datetime'],
                    y: [
                        parseFloat(value['open']).toFixed(2),
                        parseFloat(value['high']).toFixed(2),
                        parseFloat(value['low']).toFixed(2),
                        parseFloat(value['close']).toFixed(2),
                        ],
                }));
                this.series = [{
                    data: this.seriesData
                }];
                const yValues = this.seriesData.flatMap(point => point.y);
                this.min = Math.min(...yValues) + 1;
                this.max = Math.max(...yValues) + 1;
                this.chartOptions['yaxis']['max'] = this.max.toFixed(0);
                //console.log(this.min);    DEBUG
                this.chartOptions['yaxis']['min'] = this.min.toFixed(0);
                //console.log(this.max)     DEBUG
            }
            const newspath = 'http://127.0.0.1:5000/news/' + this.$route.params.Ticker + '/stocks';
            const newsres = await axios.get(newspath);
            if(!newsres.code){
                this.newslst = newsres.data
            }
        },
        async refreshPage(){
            await this.getData()
            this.chartOptions['xaxis']['tickAmount'] = this.tickSON[this.text]
        },
        async searchBar(){
            window.location.reload();
        }
    },
    created(){
        this.getData();
    },
}
</script>
<style>
.button_container{
    padding-top:75px;
    padding-left:20px;
    padding-bottom:30px;
    padding-right:0px;
}
.chart_container{
    padding-left:20px;
}
.logo_container{
    transform: scale(.25);
    transform-origin: left;
    margin-top:0px;
    margin-bottom:0px;
    margin-right:0px;
    margin-left:0px;
    padding-top:0px;
    padding-left:0px;
    padding-bottom:0px;
    padding-right:0px;
}
.apexcharts-tooltip{
    color:black
}
.news_container{
    list-style-type:none;
    display:flex;
    flex-direction: row;
}
</style>