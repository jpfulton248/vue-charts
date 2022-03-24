<template>
  <div>
    <div class="custom">
      <label> Select Property: </label>
      <select @change="ChangeProperty">
        <option>Select Property..</option>
        <option value="straddle">Straddle</option>
        <option value="impliedmove">ImpliedMove</option>
        <option value="underlying">Underlying</option>
        <option value="strike">Strike</option>
        <option value="quarter">Quarter</option>
      </select>
    </div>
    <apexchart
      width="800"
      class="custom"
      type="bar"
      :options="options"
      :series="series"
      ref="chart"
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
      straddle: [],
      impliedmove: [],
      underlying: [],
      strike: [],
      quarter: [],

      options: {
        chart: {
          id: "vuechart-example",
        },
        xaxis: {
          // type: 'categories'
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
          name: "property",
          data: data,
        },
      ],
    };
  },
  methods: {
    getAllData() {
      axios.get("http://127.0.0.1:5000/get-all-changes").then((res) => {
        data = res.data;
        console.log("data>>", data);

        data.forEach((element) => {
          this.id = 0;
          let a = element["straddle"];
          this.getStraddleProperty(a);
          let b = element["impliedmove"];
          this.getImpliedMoveProperty(b);
          let c = element["underlying"];
          this.getUnderlyingProperty(c);
          let d = element["strike"];
          this.getStrikeProperty(d);
          let f = element["quarter"];
          this.getQuarterProperty(f);
          this.id = element["changesid"];
        });
        console.log("lastid>>>", this.id);
      });
    },
    getStraddleProperty(a) {
      let val = a;
      this.straddle.push(val);
    },
    getImpliedMoveProperty(b) {
      let val = b;
      this.impliedmove.push(val);
    },
    getUnderlyingProperty(c) {
      let val = c;
      this.underlying.push(val);
    },
    getStrikeProperty(d) {
      let val = d;
      this.strike.push(val);
    },
    getQuarterProperty(f) {
      let val = f;
      this.quarter.push(val);
    },
    ChangeProperty(e) {
      let dataArray = e.target.value;
      console.log(dataArray);
      switch (dataArray) {
        case "straddle":
          dataArray = this.straddle;
          break;
        case "impliedmove":
          dataArray = this.impliedmove;
          break;
        case "underlying":
          dataArray = this.underlying;
          break;
        case "strike":
          dataArray = this.strike;
          break;
        case "quarter":
          dataArray = this.quarter;
          break;
      }
      this.chartOptions.series.data = dataArray;
      console.log(this.chartOptions.series.data);
    },
    getLatestData() {
      axios.get("http://127.0.0.1:5000/get-last-changes").then((res) => {
        let x = res.data;
        if (x.changesid == this.id) {
          console.log("no updates...")
          this.getAllData();
          return;
        } else {
          data.push(x);
          this.getAllData();
          console.log("update added>>>>", data)
        }
      });
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