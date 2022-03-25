<template>
  <div>
    <div class="custom">
      <label> Select Property: </label>
      <select @change="ChangeProperty">
        <option value="straddle" selected>Straddle</option>
        <option value="impliedmove">ImpliedMove</option>
        <option value="underlying">Underlying</option>
        <option value="strike">Strike</option>
        <option value="quarter">Quarter</option>
      </select>
    </div>
    <apexchart
      ref="chart"
      width="800"
      class="custom"
      type="line"
      :options="options"
      :series="series"
    ></apexchart>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";
import axios from "axios";

var data = [];

export default {
  name: "app",
  components: {
    apexchart: VueApexCharts,
  },
  data: function () {
    return {
      intervalid1: "",
      id: null,
      existingData: [],
      property: "straddle",

      options: {
        chart: {
          id: "vuechart-example",
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
            },
          },
        ],
        tooltip: {
          x: {
            format: "dd MMM yyyy",
          },
        },
      },
      series: [
        {
          name: "straddle",
          data: data,
        },
      ],
    };
  },
  methods: {
    getAllData() {
      axios.get("http://127.0.0.1:5000/get-all-changes").then((res) => {
        this.existingData = res.data;
        this.renderProperty();
      });
    },

    renderProperty() {
      data = [];
      this.existingData.forEach((element) => {
        let date = new Date(element["dated"]).getTime();
        data.push({
          x: date,
          y: element[this.property],
        });

        this.id = element["changesid"];
      });

      this.$refs.chart.updateSeries([
        {
          data: data,
        },
      ]);
    },
    ChangeProperty(e) {
      this.property = e.target.value;
      this.renderProperty();
    },
    getLatestData() {
      axios.get("http://127.0.0.1:5000/get-last-changes").then((res) => {
        let result = res.data;
        if (result.changesid == this.id) {
          return;
        } else {
          this.existingData.push(result);
          this.updateSeries(result);
        }
      });
    },
    updateSeries(result) {
      let date = new Date(result["dated"]).getTime();
      data.push({
        x: date,
        y: result[this.property],
      });
      this.$refs.chart.updateSeries([
        {
          data: data,
        },
      ]);
    },
    start() {
      let that = this;
      this.intervalid1 = setInterval(() => {
        that.getLatestData();
      }, 5000);
    },
  },
  mounted: function () {
    this.getAllData();
    this.start();
  },
  beforeUnmount() {
    clearInterval(this.intervalid1);
  },
};
</script>

<style>
.text-center {
  align-items: center;
  margin: 40px;
  padding: 40px;
}
.custom {
  padding: 20px;
}
</style>