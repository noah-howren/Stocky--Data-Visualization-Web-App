<template>
    <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
import { initializeApp } from "firebase/app";
const firebaseConfig = {
    apiKey: import.meta.env.FIR_API,
    authDomain: "stocky-data.firebaseapp.com",
    projectId: "stocky-data",
    storageBucket: "stocky-data.firebasestorage.app",
    messagingSenderId: "859550902029",
    appId: import.meta.env.FIR_APP,
    measurementId: "G-3QG3MJEWZ1"
};

const app = initializeApp(firebaseConfig);

</script>
<style>
    .rubik { 
        font-family: "Rubik", sans-serif; 
    }
</style>