<template>
  <div id="chart" class="text-center">
    <apexchart
      ref="chart"
      width="800"
      height="450"
      type="line"
      :options="options"
      :series="series"
    ></apexchart>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";
var data = [];

export default {
  name: "app",
  components: {
    apexchart: VueApexCharts,
  },
  data: function () {
    return {
      options: {
        chart: {
          id: "vuechart-example",
          height: 350,
          type: "line",
          animations: {
            enabled: true,
            easing: "linear",
            dynamicAnimation: {
              speed: 1000,
            },
          },
        },
        title: {
          text: "Dynamic Earnings Chart",
          align: "center",
        },
        toolbar: {
          show: true,
        },
        zoom: {
          enabled: true,
            type: "x",
            resetIcon: {
              offsetX: -10,
              offsetY: 0,
            }
          },
        stroke: {
          curve: "smooth",
        },
        xaxis: {
          type: "datetime",
        },
        yaxis: [
          {
            min: (min) => {
              return min; 
            },
            max: (max) => {
              return max; 
            }
          }
         
        ],
        tooltip: {
          x: {
            format: 'dd MMM yyyy',
          },
        },
      },
      series: [
        {
          name: "price",
          data: data,
        },
      ],
    };
  },
  methods: {
    connectWebSocket() {

    
      let that = this;

      const socket = new WebSocket("ws://127.0.0.1:5000/get-updated-data");

      socket.onopen = function () {
        console.log("Connection Success!!!");
      };

      socket.onmessage = function (event) {
        let x = event.data;
        that.updateSeries(x);
      };

      socket.onclose = function () {
        console.log("[Close] connection Closed");
      };
    },

    updateSeries(x) {
      x = JSON.parse(x);
      let date = new Date(x["exactearningsdate"]).getTime();
      data.push({
        date: x["exactearningsdate"],
        x: date,
        y: x["averageoptionvol"],
      });

      console.log("data>>>>>", data); 

      this.$refs.chart.updateSeries([
        {
          data: data,
        },
      ]);
    },

  },
  mounted: function () {
    setTimeout(() => {
      this.connectWebSocket();
    }, 1000);
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