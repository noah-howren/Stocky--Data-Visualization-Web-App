import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config';
import './assets/main.css';
import Listbox from 'primevue/listbox';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice';
import Vue3Marquee from 'vue3-marquee'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/dist/vuetify.css'
import '@fontsource-variable/rubik';


const myCustomDark = {
  dark: true,
  colors: {
    background: '#181818',
    surface: '#181818'
  }
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'myCustomDark',
    themes: {
      myCustomDark,
    }
  },
});
const app = createApp(App)
app.use(PrimeVue)
app.use(router)
app.use(ToastService)
app.use(vuetify)
app.use(Vue3Marquee)
app.component('v-combobox', components.VCombobox)
app.component('v-select', components.VSelect)
app.component('v-btn', components.VBtn)
app.component('v-btn-toggle', components.VBtnToggle)
app.component('v-app-bar', components.VAppBar)
app.component('v-app', components.VApp)
app.component('v-spacer', components.VSpacer)
app.component('v-system-bar', components.VSystemBar)
app.component('Button', Button)
app.component('Listbox', Listbox)
app.component('Toast', Toast)
app.component('MarqueeComponent', Vue3Marquee)
app.mount('#app')
