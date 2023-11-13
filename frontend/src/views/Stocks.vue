<template>
    <div class="whole_container">
        <div class="logo_container">
            <img :src="image">
        </div>
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
    </div>
</template>

<script>
import img from '@/assets/stocky_logo.png';
import axios from 'axios';
import ApexCharts from 'vue3-apexcharts';
export default{
    components: {
          apexchart: ApexCharts,
    },
    data(){
        console.log('hello')
        return{
            text: 'd',
            image:img,
            data:[],
            seriesData:[],
            series:[],
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
                    labels:{
                        formatter: function(value){
                            return "$"+value;
                        },
                        style:{
                            colors:'white'
                        }
                    }
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
        selectedInterval(newValue, oldValue) {
            if (newValue !== oldValue) {
                this.refreshPage();
            }
        }
    },
    methods:{
        async getData() {
            console.log('hi')
            const path = 'http://127.0.0.1:5000/query/' + this.$route.params.Ticker + '/' +this.selectedInterval;
            const res = await axios.get(path)
            if(!res.code){
                this.seriesData = Object.entries(res.data).map(([key, value]) => ({
                    x: value['datetime'],
                    y: [
                        parseFloat(value['open']),
                        parseFloat(value['high']),
                        parseFloat(value['low']),
                        parseFloat(value['close']),
                        ],
                }));
                this.series = [{
                    data: this.seriesData
                }];
            }
        },
        async refreshPage(){
            console.log('test')
            await this.getData()
            this.chartOptions['xaxis']['tickAmount'] = this.tickSON[this.text]
            //ApexCharts.exec('candles', 'updateSeries', [{data: this.series}], true)
            //ApexCharts.exec('candles', 'updateOptions', this.chartOptions, false, true)
        }
    },
    created(){
        this.getData();
    },
}
</script>
<style>
.button_container{
    padding-top:0px;
    padding-left:0px;
    padding-bottom:30px;
    padding-right:0px;
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
</style>