<template>
    <v-app app theme="myCustomDark">
        <nav_bar></nav_bar>
        <img :src="background" class="background" :key="background">
        <div class="content-wrapper">
            <div class="chart_header">Key Market Indicies</div>
            <div class="chart-container">
                
                <div class="chart-box">
                    <h3 class="chart-title">S&P 500</h3>
                    <apexchart
                        class="spy"
                        type="line"
                        :height="300"
                        :width="500"
                        :series="spyData"
                        :options="spyOpt"
                    />
                </div>
                
                <div class="chart-box">
                    <h3 class="chart-title">NASDAQ Composite</h3>
                    <apexchart
                        class="comp"
                        type="line"
                        :height="300"
                        :width="500"
                        :series="compData"
                        :options="compOpt"
                    /> 
                </div>
                <div class="chart-box">
                    <h3 class="chart-title">Invesco QQQ Trust</h3>
                    <apexchart
                        class="qqq-graph"
                        type="line"
                        :height="300"
                        :width="500"
                        :series="spyData"
                        :options="spyOpt"
                    /> 
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
            this.getData();
        },
        components: {
            nav_bar,
            apexchart: ApexCharts
        },
        data() {
            return {
                background: s_background,
                qqqData: [],
                spyData: [],
                compData: [],
                rutData: [],
                news: [],
                newsData: [],
                isNews: false,
                qqqOpt: {
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
                        colors: ['#04ff00']  // Same green color as other charts
                    }
                },
                spyOpt: {
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
                },
                compOpt: {
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
                const path = `http://127.0.0.1:5000/homepage/`;
                try {
                    const response = await axios.get(path);
                    console.log('Raw API response:', response.data);
                    const { comp, qqq, news, spy} = response.data;
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
                    this.qqqData = this.processChartData(qqq);
                    this.spyData  = this.processChartData(spy);
                    this.compData = this.processChartData(comp);
                } catch (error) {
                    console.error('Error fetching data:', error);
                }
            },
            updateBackground() {
            if (this.$route.path.startsWith('/crypto/')) {
                document.title = "Stocky | Crypto"
                this.background = c_background
            } else {
                document.title = "Stocky | Stocks"
                this.background = s_background
            }
            },
            reloadBackground() {
                this.background = this.background + '?t=' + new Date().getTime();
            },
            processChartData(chartData) {
                if (!Array.isArray(chartData) || chartData.length === 0) {
                    return [];
                }
                console.log('Raw chart data:', chartData);
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

.chart_header {
    color: white;
    font-size: 30px;
    font-style: italic;
    font-weight: bold;
    margin-bottom: 0px;
    margin-left: auto;
    margin-right: auto;
    max-width: fit-content;
}
.chart-container {
    display: flex;
    max-width: fit-content;
    margin-left:auto;
    margin-right:auto;
    margin-inline: auto;
    flex-direction: row;
    justify-content: center;
    align-items: flex-start;
    gap: 32px;
    padding: 20px;
    flex-wrap: wrap;
}

.chart-box {
    background: rgba(0, 0, 0, 0.8);
    border-radius: 8px;
    padding: 16px;
    min-width: 400px;
}

.chart-title {
    color: white;
    margin-bottom: 16px;
    font-size: 18px;
    font-weight: 500;
    text-align: center;
}

.custom-font {
    font-family: 'Rubik', sans-serif;
}

.chart-box {
    background: rgba(0, 0, 0, 0.8);
    border-radius: 8px;
    padding: 16px;
    min-width: 400px;
}

.news_section {
    padding-left: 20px;
    width: 100%;
}

.news_header {
    color: white;
    font-size: 30px;
    font-style: italic; 
    font-weight: bold;
    margin-left: auto;
    margin-top: 0px;
    margin-right: auto;
    padding-bottom: 20px;
    max-width: fit-content;
}

.news_container {
    display: flex;
    justify-content: flex-start;
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
    width: 531px;
    flex-direction: column;
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