<template>
    <div>
        <p v-if="msg">{{ msg }}</p>
        <p v-else>1111...</p>
    </div>
</template>

<script>
import axios from 'axios';
import { VueElement } from 'vue';

export default{
    name: 'Test',
    data() {
        return {
            msg: '',
        };
    },
    methods: {
        async getMessage() {
            console.log('hi')
            const path = 'http://127.0.0.1:5000/';
            const res = await axios.get(path)
                if(!res.code){
                    this.msg = res.data; 
                };
        },
    },
    created(){
        this.getMessage();
    },
};
</script>