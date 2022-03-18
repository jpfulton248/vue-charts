<template>
<div id="app"> 
  <Chart />
  <!-- <RealTimeStaticChart/> -->
  <!-- <ChartLine/> -->
  
</div>
</template>

<script>
import Chart from './components/Chart.vue';
// import RealTimeStaticChart from './components/RealTimeStaticChart.vue';
// import ChartLine from './components/ChartLine.vue';

export default {
  name: 'App',
  components: {
  Chart,
  // RealTimeStaticChart,
  // ChartLine
  }
}
</script>

<style>
.container {
  margin: 0 auto;
  width: 100%;
  display: grid;
  gap: 2rem;
}
@media (min-width: 1024px) {
  .container {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
.chart-container {  
  background-color: #f5f4f3;
  border-radius: 0.5rem;
}
</style>
