<template>
    <v-app app theme="myCustomDark">
        <nav_bar></nav_bar>
        <img :src="background" class="background" :key="background">
        <div class="content-wrapper">
            <div class="chart-container">
                <div class="chart-box">
                    <h3 class="chart-title">DOW Jones Industrial Average</h3>
                    <apexchart
                        class="djia"
                        type="line"
                        :height="300"
                        :width="500"
                        :series="compData"
                        :options="compOpt"
                    /> 
                </div>
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
                djiaData: [],
                spyData: [],
                compData: [],
                rutData: [],
                djiaOpt: {
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
                    }
                },
                chartOptions: {
                    chart: {
                        type: 'line',
                        height: '30%',
                        width: 400,
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
                    const { djia, spy, comp } = response.data;
                    this.djiaData = this.processChartData(djia);
                    this.spyData  = this.processChartData(spy);
                    this.compData = this.processChartData(comp);
                    this.djiaOpt  = this.getChartOptions(this.djiaData, {...this.chartOptions});
                    this.spyOpt   = this.getChartOptions(this.spyData, {...this.chartOptions});
                    this.compOpt  = this.getChartOptions(this.compData, {...this.chartOptions});
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
            },
            getChartOptions(chartData, chartOpt)
            {
                console.log(chartData);
                const yValues = chartData.flatMap(point => point.y.map(Number));
                if (yValues.length > 0) {
                    console.log((Math.min(...yValues) - 1).toFixed(0));
                    console.log((Math.max(...yValues) + 1).toFixed(0));
                    chartOpt.yaxis.max = (Math.max(...yValues) + 1).toFixed(0);
                    chartOpt.yaxis.min = (Math.min(...yValues) - 1).toFixed(0);
                }
                return chartOpt;
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
    background: transparent !important; /* Transparent to show your background GIF */
    box-shadow: none; /* Remove any shadows, if present */
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
    padding-top: 164px;
    position: relative;
    z-index: 1;
    font-family: 'Rubik', sans-serif;
}

.chart-container {
    display: flex;
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
</style>