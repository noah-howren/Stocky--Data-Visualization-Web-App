<template>
    <v-app app theme="myCustomDark">
        <div class="whole_container">
            <nav_bar></nav_bar>
            <div class="content_container">
                <div class="chart_section">
                    <div v-if =isFetching class="info_container">
                        <div v-show="logoLoaded" class="comp_logo">
                            <img :src="logo_src" alt="Logo" @error="handleLogoError" @load="handleLogoLoad">
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
                <div v-if =isNews class="news_section">
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
            rawChartData: [],
            logoLoaded: false,
            isFetching: false,
            isNews: false,
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
        },
        '$route.params.Ticker': {
            immediate: true,
            handler() {
                this.resetLogoState();
            }
        }
    },
    methods: {
        async getData() {
            this.tick = this.$route.params.Ticker;
            const path = `http://127.0.0.1:5000/query/stocks/${this.$route.params.Ticker}/${this.selectedInterval}`;
            try {
                const response = await axios.get(path);
                const { chartData, newsData, infoData } = response.data;
                this.name = infoData?.name || '';
                this.logo_src = `https://assets.parqet.com/logos/symbol/${this.tick}?format=png`;
                
                this.rawChartData = chartData; // Store the raw chart data
                this.processChartData(); // Process the chart data
                if (newsData.length == 0){
                    this.isNews = false;
                }
                else{
                    this.processNewsData(newsData);
                }
                this.isFetching = true;
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        processChartData() {
            if (Array.isArray(this.rawChartData) && this.rawChartData.length > 0) {
                this.seriesData = this.rawChartData.map(value => ({
                    x: value.datetime,
                    y: [
                        parseFloat(value.open || 0).toFixed(2),
                        parseFloat(value.high || 0).toFixed(2),
                        parseFloat(value.low || 0).toFixed(2),
                        parseFloat(value.close || 0).toFixed(2)
                    ]
                }));

                this.series = [{ data: this.seriesData }];

                const yValues = this.seriesData.flatMap(point => point.y.map(Number));
                if (yValues.length > 0) {
                    this.min = Math.min(...yValues);
                    this.max = Math.max(...yValues);
                    this.chartOptions.yaxis.max = (this.max + 1).toFixed(0);
                    this.chartOptions.yaxis.min = (this.min - 1).toFixed(0);
                }
            } else {
                console.warn('No valid chart data available');
                this.seriesData = [];
                this.series = [];
                this.chartOptions.yaxis.max = null;
                this.chartOptions.yaxis.min = null;
            }
            this.chartOptions.xaxis.tickAmount = this.tickSON[this.text] || 39;

        },
        processNewsData(newsData) {
            if (newsData && newsData.length > 0) {
                this.newslst = newsData.slice(0, 3); // Limit to 3 articles
                this.newsData = true;
            } else {
                console.error('No news data available');
            }
        },
        async refreshGraph() {
            const path = `http://127.0.0.1:5000/refreshGraph/stocks/${this.$route.params.Ticker}/${this.selectedInterval}`;
            try {
                const response = await axios.get(path);
                this.rawChartData = response.data;
                this.processChartData();
            }
            catch (error) {
                console.error('Error fetching data:', error);
            }
            this.processChartData(this.seriesData);
        },
        async refreshPage() {
            await this.getData(); // Update the graph
        },
        async searchBar() {
            window.location.reload();
        },
        resetLogoState() {
            this.logoLoaded = false;
            this.logo_src = `https://assets.parqet.com/logos/symbol/${this.$route.params.Ticker}?format=png`;
        },
        handleLogoError() {
            this.logoLoaded = false;
        },
        handleLogoLoad() {
            this.logoLoaded = true;
        }
    },
    created() {
        this.getData();
    }

}
</script>

<style>
.whole_container{
    font-family: "Rubik", sans-serif;
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
.nav-bar{
    z-index: 1000;
    position:sticky;
    padding: 0px;
}
.info_container{
    margin-top:10px;
    margin-left:30px;
    margin-bottom:5px;
    display: flex;
    align-items: flex-start; 
}
.comp_logo{
    margin-right: 18px;
    padding-top: 10px;
}
.content_container {
    display: flex;
    justify-content: space-between;
    max-width: 20%;
    align-items: flex-start;
}

.info_text{
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
    margin-bottom: 10px;
    margin-left:30px;
    margin-top:0px !important;
    padding: 0px !important;
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