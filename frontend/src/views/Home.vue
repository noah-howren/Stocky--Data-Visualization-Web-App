<template>
    <v-app app theme="myCustomDark">
        <nav_bar></nav_bar>
        <img :src="background" class="background" :key="background">
        <div class="content-wrapper">
            <div v-show =isCharts class="chart_section">
                <div class="chart_header">{{chartCaption}}</div>
                <div class="chart_container">
                    <div v-for="(chart, index) in chartData" :key="index" class="chart_box">
                        <h3 class="chart_title">{{chart.title}}</h3>
                        <apexchart
                            class="spy"
                            type="line"
                            :height="300"
                            :width="500"
                            :series="chart.data"
                            :options="chart.chartOpt"
                        />
                    </div>
                </div>
            </div>
            <div v-show =isNews class="news_section">
                <div class="news_header">Market News</div>
                    <div class="news_container" v-if="newsData.length > 0">
                        <div v-for="(article, index) in newsData" :key="index" class="news_box">
                            <v-img :src="article.image_url" height="120px" width="100%" cover></v-img>
                            <h3 class="news_title">{{ article.title }}</h3>
                            <a :href="article.url" target="_blank" class="news_link">Read More</a>
                    </div>
                </div>
            </div>
        </div>
    </v-app>
</template>

<script>
    import nav_bar from '@/components/nav_bar/nav_bar.vue'
    import s_background from '@/assets/bg.gif'
    import c_background from '@/assets/bg_crypto.gif'
    import axios from 'axios'
    import ApexCharts from 'vue3-apexcharts';
    export default {
        mounted() {
            document.title = "Stocky | Stocks";
            this.updateBackground()
        },
        components: {
            nav_bar,
            apexchart: ApexCharts
        },
        data() {
            return {
                background: s_background,
                chartData: [],
                news: [],
                newsData: [],
                isNews: false,
                isCharts: false,
                chartCaption: 'Key Market Indicies',
                chartOptions: {
                    chart: {
                        type: 'line',
                        id: 'lines',
                        fontFamily: 'Rubik, sans-serif'
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
                        tickAmount: 10,
                        labels: {
                            style: {
                                colors: 'white'
                            }
                        }
                    },
                    stroke: {
                        curve: 'smooth',
                        width: 2
                    },
                    fill: {
                        type: 'solid',
                        colors: ['#04ff00']
                    }
                }
            }
        },
        watch: {
            $route(to, from) {
            this.updateBackground();
            }
        },
        methods: {
            async getData(){
                const path = `http://127.0.0.1:5000/homepage` + this.$route.path;
                try {
                    const response = await axios.get(path);
                    const { data, news} = response.data;
                    if (news.length > 0){
                        this.isNews = true;
                        this.newsData = news;
                        console.log(this.newsData);
                    }
                    else{
                        this.isNews = false;
                        this.newsData = [];
                        console.log("no news!");
                    }
                    if (data.length > 0){
                        this.isCharts = true;
                        this.chartData = [];
                        for (const dataset of data)
                        {
                            console.log(dataset.Title);
                            const chrtOpt = JSON.parse(JSON.stringify(this.chartOptions));
                            chrtOpt.fill.colors = [dataset.Fill];
                            this.chartData.push({'title':dataset.Title, 'data':this.processChartData(dataset.Data), 'chartOpt':chrtOpt});
                        }
                    }
                    else{
                        this.isCharts = false;
                        this.chartData = [];
                        console.log("no charts!");
                    }
            
                } catch (error) {
                    console.error('Error fetching data:', error);
                }
            },
            updateBackground() {
                if (this.$route.path.startsWith('/crypto/')) {
                    document.title = "Stocky | Crypto";
                    this.background = c_background;
                    this.chartCaption = "Top Cryptocurrencies";
                } else {
                    document.title = "Stocky | Stocks";
                    this.background = s_background;
                    this.chartCaption = "Key Market Indicies";
                }
                this.getData();
            },
            reloadBackground() {
                this.background = this.background + '?t=' + new Date().getTime();

            },
            processChartData(chartData) {
                if (!Array.isArray(chartData) || chartData.length === 0) {
                    return [];
                }
                return [{
                    name: 'Price',
                    data: chartData.map(item => ({
                        x: item.datetime,
                        y: parseFloat(item.close)
                    }))
                }];
            }
        }
    }
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
}

.v-theme--myCustomDark {
    background: transparent !important;
    box-shadow: none; 
}

.background {
    position: fixed;
    left: 0;
    right: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -1;
    filter: saturate(50%) brightness(30%);
}

.content-wrapper {
    padding-top: 140px;
    position: relative;
    z-index: 1;
    font-family: 'Rubik', sans-serif;
}

.custom-font {
    font-family: 'Rubik', sans-serif;
}

.chart_title {
    color: white;
    margin-bottom: 16px;
    font-size: 18px;
    font-weight: 500;
    text-align: center;
}
.chart_box {
    background: rgba(0, 0, 0, 0.8);
    border-radius: 8px;
    padding: 16px;
    min-width: 450px;
}

.chart_section, .news_section {
    padding-left: 20px;
    width: 100%;
    max-width: 100%;
    align-items: center !important;
}

.news_header, .chart_header{
    color: white;
    font-size: 30px;
    font-style: italic; 
    font-weight: bold;
    margin-left: auto;
    margin-top: 20px;
    margin-right: auto;
    padding-bottom: 20px;
    max-width: fit-content;
}

.chart_container, .news_container {
    display: flex;
    justify-content: center;
    margin-left: auto;
    margin-right: auto;
    flex-direction: row;
    align-items: stretch;
    flex-wrap: wrap;
    gap:32px;
}

.news_box {
    background: rgba(0, 0, 0, 0.8);
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 532px;
    flex-direction: column;
    margin: 0; 
}

.news_title {
    padding: 10px;
    color: white;
    font-size: 14px;
    margin: 0;
    line-height: 1.2;
    flex-grow: 1;
}

.news_link {
    display: block;
    padding: 5px 10px;
    color: #4CAF50;
    text-decoration: none;
    font-size: 12px;
    margin-top: auto;
} 

.news_link:hover {
    text-decoration: underline;
}

/* Make sure images in news boxes maintain aspect ratio */
.news_box .v-img {
    width: 535px;
    height: auto;
    object-fit: cover;
}

</style>