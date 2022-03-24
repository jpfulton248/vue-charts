<template>
  <div id="app" class="container">
    <div class="row">
      <!-- <Chart /> -->
    </div>
     <div class="row">
      <Changes />
    </div>
    <div class="row">
      <!-- <RealTimeStaticChart /> -->
    </div>
    <div class="row custom" >
      <!-- <ChartLine /> -->
    </div>
  </div>
</template>

<script>
// import Chart from "./components/Chart.vue";
import Changes from "./components/Changes.vue";
// import RealTimeStaticChart from "./components/RealTimeStaticChart.vue";
// import ChartLine from "./components/LineChart.vue";

export default {
  name: "App",
  components: {
    // Chart,
    Changes,
    // RealTimeStaticChart,
    // ChartLine,
  },
};
</script>

<style>
.container {
  margin: 0 auto;
  width: 100%;
  display: grid;
  gap: 2rem;
}

.chart-container {
  background-color: #f5f4f3;
  border-radius: 0.5rem;
}

/* @media (min-width: 1024px) {
  .container {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
} */
.custom{
  padding: 40px;
}
</style>
