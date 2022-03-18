<template>
  <!-- this chart is made using realtime apexcharts but with static data  -->
  <div id="app">
    <div id="chart">
      <apexchart
        ref="realtimeChart"
        type="line"
        height="350"
        :options="chartOptions"
        :series="series"
      />
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

var lastDate = 0;
var data = [];

function getDayWiseTimeSeries(baseval, count, yrange) {
  var i = 0;
  while (i < count) {
    var x = baseval;
    var y =
      Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
    console.log(x, y);
    data.push({
      x,
      y,
    });
    lastDate = baseval;
    baseval += 86400000;
    i++;
  }
} 

getDayWiseTimeSeries(new Date("11 Feb 2017 GMT").getTime(), 10, {
  min: 10,
  max: 90,
});

function getNewSeries(baseval, yrange) {
  var newDate = baseval + 86400000;
  lastDate = newDate;
  data.push({
    x: newDate,
    y: Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min,
  });
}

function resetData() {
  data = data.slice(data.length - 10, data.length);
}

export default {
  name: "app",
  components: {
    apexchart: VueApexCharts,
  },
  data: function () {
    return {
      series: [
        {
          data: data.slice(),
        },
      ],
      chartOptions: {
        chart: {
          animations: {
            enabled: true,
            easing: "linear",
            dynamicAnimation: {
              speed: 2000,
            },
          },
          toolbar: {
            show: true,
          },
          zoom: {
            enabled: true,
          },
        },
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: "smooth",
        },

        title: {
          text: "Earnings dynamic chart",
          align: "left",
        },
        markers: {
          size: 0,
        },
        xaxis: {
          type: "datetime",
          range: 777600000,
        },
        yaxis: {
          max: 100,
        },
        legend: {
          show: false,
        },
      },
    };
  },
  mounted: function () {
    this.intervals();
  },
  methods: {
    intervals: function () {
      var me = this;
      window.setInterval(function () {
        getNewSeries(lastDate, {
          min: 10,
          max: 90,
        });

        me.$refs.realtimeChart.updateSeries([
          {
            data: data,
          },
        ]);
      }, 2000);

      // every 60 seconds, we reset the data
      window.setInterval(function () {
        resetData();
        me.$refs.realtimeChart.updateSeries(
          [
            {
              data,
            },
          ],
          false,
          true
        );
      }, 60000);
    },
  },
};
</script>

<style>
.text-center {
  align-items: center;
  margin: 40px;
  padding: 40px;
}
</style>