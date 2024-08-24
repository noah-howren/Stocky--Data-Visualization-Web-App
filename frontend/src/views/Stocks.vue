<template>
    <v-app app theme="myCustomDark">
        <div class="whole_container">
            <nav_bar></nav_bar>
            <div class="content_container">
                <div class="chart_section">
                    <div class="info_container">
                        <div class="comp_logo">
                            <img :src="logo_src" alt="Logo">
                        </div>
                        <div class="info_text">
                            {{ name }}
                            <div class="ticker_text">
                                {{ tick }}
                            </div>
                        </div>
                    </div>
                    <div class="button_container">
                        <v-btn-toggle
                            v-model="text"
                            rounded="10"
                            color="green-accent-4"
                            divided
                            @update="refreshPage"
                        >
                            <v-btn value="d">Day</v-btn>
                            <v-btn value="w">Week</v-btn>
                            <v-btn value="m">Month</v-btn>
                            <v-btn value="y">Year</v-btn>
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
                <div class="news_section">
                    <div class="news_header">Related News:</div>
                    <div class="news_container" v-if="newslst.length > 0">
                        <div v-for="(article, index) in newslst" :key="index" class="news_box">
                            <v-img :src="article.image_url" height="120px" width="100%" cover></v-img>
                            <h3 class="news_title">{{ article.title }}</h3>
                            <a :href="article.url" target="_blank" class="news_link">Read More</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </v-app>
</template>

<script>
import img from '@/assets/stocky_logo.png';
import axios from 'axios';
import ApexCharts from 'vue3-apexcharts';
import nav_bar from '@/components/nav_bar/nav_bar.vue';

export default {
    mounted() {
        document.title = "Stocky | " + this.$route.params.Ticker;
    },
    components: {
        apexchart: ApexCharts,
        nav_bar
    },
    data() {
        return {
            text: 'd',
            image: img,
            seriesData: [],
            series: [],
            newslst: [],
            tick: '',
            logo_src: '',
            name:'',
            tickSON: {
                'd': '39',
                'w': '21',
                'm': '30',
                'y': '63'
            },
            chartOptions: {
                chart: {
                    type: 'candlestick',
                    height: 200,
                    width: 1200,
                    id: 'candles'
                },
                zoom: {
                    enabled: false
                },
                title: {
                    align: 'left',
                    style: {
                        color: 'white',
                        fontSize: '16px',
                        fontWeight: 'bold'
                    }
                },
                tooltip: {
                    enabled: true,
                    followCursor: true,
                    style: {
                        color: 'black'
                    }
                },
                yaxis: {
                    forceNiceScale: true,
                    labels: {
                        formatter: function(value) {
                            return '$' + value.toFixed(2);
                        },
                        style: {
                            colors: 'white'
                        }
                    }
                },
                xaxis: {
                    tickAmount: 39,
                    labels: {
                        style: {
                            colors: 'white'
                        }
                    }
                }
            }
        }
    },
    computed: {
        selectedInterval() {
            return this.text;
        }
    },
    watch: {
        '$route.params': 'searchBar',
        selectedInterval(newValue, oldValue) {
            if (newValue !== oldValue) {
                this.refreshPage();
            }
        }
    },
    methods: {
        async getData() 
        {
            this.tick = this.$route.params.Ticker;
             
            const path = `http://127.0.0.1:5000/query/stocks/${this.$route.params.Ticker}/${this.selectedInterval}`;
            
            try {
                const response = await axios.get(path);
                const { chartData, newsData, infoData} = response.data;
                this.name = infoData['name']
                this.logo_src = `https://assets.parqet.com/logos/symbol/${this.tick}?format=png`
                console.log(this.logo_src)
                // Process chart data
                if (chartData && chartData.length > 0) {
                    this.seriesData = chartData.map(value => ({
                        x: value.datetime,
                        y: [
                            parseFloat(value.open).toFixed(2),
                            parseFloat(value.high).toFixed(2),
                            parseFloat(value.low).toFixed(2),
                            parseFloat(value.close).toFixed(2)
                        ]
                    }));

                    this.series = [{ data: this.seriesData }];

                    const yValues = this.seriesData.flatMap(point => point.y);
                    this.min = Math.min(...yValues) + 1;
                    this.max = Math.max(...yValues) + 1;
                    this.chartOptions.yaxis.max = this.max.toFixed(0);
                    this.chartOptions.yaxis.min = this.min.toFixed(0);
                } else {
                    console.error('No chart data available');
                }

                // Process news data
                if (newsData && newsData.length > 0) {
                    this.newslst = newsData.slice(0, 3); // Limit to 3 articles
                } else {
                    console.error('No news data available');
                }

                this.$forceUpdate();
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async refreshPage() {
            await this.getData();
            this.chartOptions['xaxis']['tickAmount'] = this.tickSON[this.text];
        },
        async searchBar() {
            window.location.reload();
        }
    },
    created() {
        this.getData();
    }
}
</script>

<style>
.nav-bar{
    z-index: 1000;
    position:sticky;
    padding: 0px;
}
.info_container{
    margin-top:10px;
    margin-bottom:35px;
    display: flex;
    align-items: flex-start; 
}
.comp_logo{
    padding-top: 10px;
}
.content_container {
    display: flex;
    justify-content: space-between;
    max-width: 20%;
    align-items: flex-start;
}

.info_text{
    margin-left: 18px;
    font-size: 50px;
    align-items: flex-start;
    color: white;
}

.ticker_text{
    font-size: 20px;
    color: white;
}
.news_header{
    margin-top:30px;
    font-size: 20px;
    color: white;
}
.chart_section {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-right: 20px;
    max-width: calc(100% - 320px);
    padding:0px !important;
}

.button_container {
    margin-bottom: 20px;
    margin-top:0px !important;
    padding: 0px !important;
}

.chart_container {
    flex: 1;
}

.news_section {
    width: 300px;
    color: white;
    align-self: flex-start;
}

.news_container {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.news_box {
    background-color: #2a2a2a;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.news_title {
    padding: 10px;
    color: white;
    font-size: 14px;
    margin: 0;
    line-height: 1.2;
}

.news_link {
    display: block;
    padding: 5px 10px;
    color: #4CAF50;
    text-decoration: none;
    font-size: 12px;
}

.news_link:hover {
    text-decoration: underline;
}
</style>