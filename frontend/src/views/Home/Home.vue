<template>
    <v-app app theme="myCustomDark">
        <nav_bar></nav_bar>
        <img :src="background" class="background" :key="background">
    </v-app>
</template>

<script>
    import nav_bar from '@/components/nav_bar/nav_bar.vue'
    import s_background from '@/assets/bg.gif'
    import c_background from '@/assets/bg_crypto.gif'
    import axios from 'axios'

    export default {
        mounted() {
            document.title = "Stocky | Stocks";
            this.updateBackground();
        },
        components: {
            nav_bar
        },
        data() {
            return {
            background: s_background
            }
        },
        watch: {
            $route(to, from) {
            this.updateBackground();
            }
        },
        methods: {
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
            }
        }
    }
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}
.background{
    height:800px;
    margin-right:10px;
    width:1800px;
}
.custom-font {
    font-family: 'Rubik', sans-serif;
}

</style>