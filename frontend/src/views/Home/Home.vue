<template>
    <v-app app theme="myCustomDark">
        <nav_bar></nav_bar>
        <img :src="background" class="background"> 
    </v-app>
</template>

<script>
    import nav_bar from '@/components/nav_bar/nav_bar.vue'
    import background from '@/assets/bg.gif'
    export default {
        mounted(){
            document.title = "Stocky | Stocks";
        },
        components: {
            nav_bar
        },
        data(){
            return{
                background:background
            }
        }
    }
</script>

<style scoped>
.background{
    height:950px;
    margin-left:0px;
    width:1800px;
}
</style>