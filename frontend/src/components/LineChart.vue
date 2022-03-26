<template>
 <!-- chartjs  -->
  <LineChart
    :chart-data="data"
    :options="options"
    css-classes="chart-container"
  />
</template>

<script setup>
import { ref, computed } from "vue"
import { LineChart } from "vue-chart-3"
import 'chartjs-adapter-luxon';
import ChartStreaming from 'chartjs-plugin-streaming';
import axios from 'axios';

import {
  Chart,
  LineController,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
} from "chart.js";

Chart.register(ChartStreaming);

Chart.register(
  LineController,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
)

Chart.defaults.set('plugins.streaming', {
  duration: 20000
});

// function getLatestData(){

//   axios.get("http://127.0.0.1:5000/get-all-earnings").then((res)=>{
//     data  = res.data
//     console.log("data>>",data)
//     data.value.forEach(x => {
//       updateSeries(x);  
//     });
    
//   })
// }

// function updateSeries(x) {
//   // x = JSON.parse(x);
//   let date = new Date(x["exactearningsdate"]).getTime();
//   console.log("date>>",date)
//   ref.chart.data.push({ 
//     x: date,
//     price : ref([x["averageoptionvol"]]) 
//   });

//   console.log("updated>>>>>", data);

//   // this.$refs.chart.updateSeries([
//   //   {
//   //     data: data,
//   //   },
//   // ]);
// }

const price = ref(data)
let data = computed(() => ({

    // labels: ['2022-02-28T08:00:00','2022-02-29T08:00:00','2022-03-01T08:00:00'],
    
    datasets: [
      {
        label: "Earnings",
        backgroundColor: "#dc322f",
        data: [
          // {
          //   x:{
             
          //     // type: "datetime",
          //     // range: 777600000, 
          //   },
          //   y: {
          //     data:[]
          //   }
          // }
        ]
      },
    ]
}))
const options = ref({
  plugins: {
    title: {
      text: "Earnings Chart"
    },
  },
  scales: {
    y:{
      data: []
    },
    x:{
        type: 'realtime',
        realtime: {
          // duration: 10000,
          // refresh: 1000,    // onRefresh callback will be called every 1000 ms
          // delay: 1000,      // delay of 1000 ms, so upcoming values are known before plotting a line
          // pause: false,     // chart is not paused
          // ttl: undefined,   // data will be automatically deleted as it disappears off the chart
          // frameRate: 30,
          

          onRefresh: chart => {
            // request data so that it can be received asynchronously
            // assume the response is an array of {x: timestamp, y: value} objects
            fetch('http://127.0.0.1:5000/get-all-earnings')
              .then(response => response.json())
              .then(data => {
                // append the new data array to the existing chart data
                chart.data.datasets[0].data.push(...data);
                console.log("hello",chart.data.datasets[0].data)
                // update chart datasets keeping the current animation
                chart.update('quiet');
              });
          }






          // onRefresh: chart => {
           
          //   setTimeout(() => {
          //     let earnings = [] 
          //     axios.get("http://127.0.0.1:5000/get-all-earnings").then((res)=>{
          //       earnings  = res.data
          //       console.log("data>>",earnings)
          //       // earnings.forEach((x)=>{
          //       //   console.log("object>>", x)
                 

                  
          //          // append the new data to the existing chart data
          //           chart.data.datasets[0].data.push(...earnings);
          //       // })
          //        console.log("object updated>>>",chart.data.datasets[0].data)
          //         // chart.data.datasets[0].data.push(...earnings);
          //         // chart.update('quite')
          //         // console.log("data??",data.value.datasets)
          //     })
          //     // .then( data => {
                
          //     //   // append the new data array to the existing chart data
          //     //   chart.data.value.datasets[0].data.push(...data);
          //     //   console.log("earnings",data)
          //     //   // update chart datasets keeping the current animation
          //     //   chart.update('quiet');
          //     // });
          //   },2000);
          // }


          // onRefresh: chart => {

          //   // query your data source and get the array of {x: timestamp, y: value} objects
          //   var data = getLatestData();

          //   // append the new data array to the existing chart data
          //   chart.data.datasets[0].data.push(...data);
          // }
        }
    }
  }
})

</script>