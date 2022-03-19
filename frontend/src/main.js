import { createApp } from 'vue'
import App from './App.vue'
import VueApexCharts from "vue3-apexcharts";
import Chart from "./plugins/chart.js"

const app = createApp(App);
app.use(VueApexCharts);
app.use(Chart);

createApp(App).mount('#app')
