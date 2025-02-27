<template>
    <v-app app theme="myCustomDark" class="app-container">
        <nav_bar></nav_bar>
        <img :src="background" class="background" :key="background">
        <div class="content-wrapper">
            <div v-show="isCharts" class="full-width-section">
                <div class="section-header">{{chartCaption}}</div>
                <div class="content-container">
                    <div v-for="(chart, index) in chartData" :key="index" class="chart-box">
                        <h3 class="chart-title">{{chart.title}}</h3>
                        <apexchart
                                type="line"
                                :height="'100%'"
                                :width="'100%'"
                                :series="chart.data"
                                :options="chart.chartOpt"
                                class="chart-container"
                            />
                    </div>
                </div>
            </div>
            
            <div v-show="isNews" class="full-width-section">
                <div class="section-header">Market News</div>
                <div class="content-container" v-if="newsData.length > 0">
                    <div v-for="(article, index) in newsData" :key="index" class="news-box">
                        <v-img :src="article.image_url" height="120px" width="100%" cover></v-img>
                        <h3 class="news-title">{{ article.title }}</h3>
                        <a :href="article.url" target="_blank" class="news-link">Read More</a>
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
                        fontFamily: 'Rubik, sans-serif',
                        parentHeightOffset: 0,
                        height: '100%',
                        width: '100%',
                        toolbar: {
                            show: false
                        },
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
                        theme: 'dark',
                        style: {
                            fontSize: '12px',
                            fontFamily: 'Rubik, sans-serif'
                        },
                        y: {
                            formatter: function(value) {
                                return '$' + value.toFixed(2);
                            },
                            title: {
                                formatter: function() {
                                    return 'Price: ';
                                },
                                style: {
                                    color: 'black',
                                    fontWeight: 'bold'
                                }
                            }
                        },
                        marker: {
                            show: true
                        },
                        // Custom tooltip styles
                        custom: function({ series, seriesIndex, dataPointIndex, w }) {
                            return '<div class="custom-tooltip">' +
                                '<span class="tooltip-label">Price: </span>' +
                                '<span class="tooltip-value">$' + series[seriesIndex][dataPointIndex].toFixed(2) + '</span>' +
                                '</div>';
                        },
                        // Additional styling for custom tooltips
                        onDatasetHover: {
                            highlightDataSeries: true,
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
                    },
                    animations: {
                        enabled: true,
                        easing: 'easeinout',
                        speed: 800,
                        animateGradually: {
                            enabled: true,
                            delay: 150
                        },
                        dynamicAnimation: {
                            enabled: true,
                            speed: 350
                        }
                    },
                    padding: {
                        top: 10,
                        right: 10,
                        bottom: 10,
                        left: 10
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
                console.log(import.meta.env.BACKEND);
                const path = `https://stocky-backend.onrender.com/homepage` + this.$route.path;
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
    box-sizing: border-box;
}

.app-container {
    width: 100vw !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow-x: hidden !important;
}

.v-theme--myCustomDark {
    background: transparent !important;
    box-shadow: none !important;
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
    width: 100% !important;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.full-width-section {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 40px;
}

.section-header {
    color: white;
    font-size: 30px;
    font-style: italic; 
    font-weight: bold;
    margin: 20px 0;
    text-align: center;
    width: 100%;
}

.content-container {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 32px;
    padding: 0 20px;
}

.chart-box {
    background: rgba(0, 0, 0, 0.8);
    border-radius: 8px;
    padding: 16px;
    width: 25%;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 300px; /* Set a fixed height */
}

.chart-title {
    color: white;
    margin-bottom: 16px;
    font-size: 18px;
    font-weight: 500;
    text-align: center;
}

.news-box {
    background: rgba(0, 0, 0, 0.8);
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 25%;
    display: flex;
    flex-direction: column;
}

.news-title {
    padding: 10px;
    color: white;
    font-size: 14px;
    margin: 0;
    line-height: 1.2;
    flex-grow: 1;
}

.news-link {
    display: block;
    padding: 5px 10px;
    color: #4CAF50;
    text-decoration: none;
    font-size: 12px;
    margin-top: auto;
} 

.news-link:hover {
    text-decoration: underline;
}

.news-box .v-img {
    width: 100%;
    height: auto;
    object-fit: cover;
}

/* Force Vuetify containers to take full width */
:deep(.v-application__wrap) {
    width: 100% !important;
    max-width: 100% !important;
}
@media (max-width: 1400px) {
    .content-container {
        flex-wrap: wrap;
    }
    
    .chart-box, .news-box {
        width: 45%;
    }
}

@media (max-width: 900px) {
    .chart-box, .news-box {
        width: 90%;
    }
}
.chart-container {
    width: 100%;
    height: calc(100% - 40px);
    flex-grow: 1;
}
</style>