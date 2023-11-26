import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config';
import './assets/main.css';
import Listbox from 'primevue/listbox';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice';
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import * as nav_bar from '@/components/nav_bar/nav_bar.vue'
import 'vuetify/dist/vuetify.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    dark: true, // Enable dark mode
    themes: {
      dark: {
        background: '#181818',
      },
    },
  },
});
const app = createApp(App)
app.use(PrimeVue)
app.use(router)
app.use(ToastService)
app.use(vuetify)
app.component('v-combobox', components.VCombobox)
app.component('v-btn', components.VBtn)
app.component('v-btn-toggle', components.VBtnToggle)
app.component('v-app-bar', components.VAppBar)
app.component('v-app', components.VApp)
app.component('v-spacer', components.VSpacer)
app.component('Button', Button)
app.component('Listbox', Listbox)
app.component('Toast', Toast)
app.mount('#app')
