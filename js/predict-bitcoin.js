/*
var btc_prices = {};
//var exchanges = ["bitfinex","bitstamp","coinbase","kraken","mtgox","cdd_binance"];
var exchanges = ["bitfinex","coinbase","mtgox","cdd_binance"];
exchanges.forEach(function(exchange) {
  btc_prices[exchange] = [];
});
var btc_prices_labels = [];

for (var i=0; i<Object.keys(combined["Time"]).length; i++) {
  exchanges.forEach(function(exchange) {
    btc_prices[exchange].push({x: combined["Time"][i], y: combined[exchange][i]});
  });
  btc_prices_labels.push(combined["Time"][i]);
}

var default_colors = ['#3366CC','#DC3912','#FF9900','#109618','#990099','#3B3EAC','#0099C6','#DD4477','#66AA00','#B82E2E','#316395','#994499','#22AA99','#AAAA11','#6633CC','#E67300','#8B0707','#329262','#5574A6','#3B3EAC']

var btc_prices_datasets = [];
for(var i=0; i<exchanges.length; i++) {
  btc_prices_datasets.push({
      label: exchanges[i],
      data: btc_prices[exchanges[i]],
      fill: false,
      borderColor: default_colors[i],
      pointRadius: 0,
      lineTension: 0,
      borderWidth: 1
  });
}

var btc_price_ctx = document.getElementById('btc_price_chart');
var btc_price_chart = new Chart(btc_price_ctx, {
  type: 'line',
  data: {
    labels: btc_prices_labels,
    datasets: btc_prices_datasets
  },
  options: {
    title: {
      display: true,
      text: 'Bitcoin Price'
    },
    scales: {
      xAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Time'
        },
        type: 'time',
        position: 'bottom'
      }],
      yAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Price'
        }
      }]
    },
    legend: {
      display: true
    },
    plugins: {
      zoom: {
        pan: {
          enabled: true,
          mode: 'x'
        },
        zoom: {
          enabled: true,
          mode: 'x'
        }
      }
    }
  }
});
*/

/*** start d3 code ***/
// 2. Use the margin convention practice 
var margin = {top: 50, right: 50, bottom: 50, left: 50}
  , width = window.innerWidth - margin.left - margin.right // Use the window's width 
  , height = window.innerHeight - margin.top - margin.bottom; // Use the window's height

// The number of datapoints
var n = 21;

// 5. X scale will use the index of our data
var xScale = d3.scaleLinear()
    .domain([0, n-1]) // input
    .range([0, width]); // output

// 6. Y scale will use the randomly generate number 
var yScale = d3.scaleLinear()
    .domain([0, 1]) // input 
    .range([height, 0]); // output 

// 7. d3's line generator
var line = d3.line()
    .x(function(d, i) { return xScale(i); }) // set the x values for the line generator
    .y(function(d) { return yScale(d.y); }) // set the y values for the line generator 
    .curve(d3.curveMonotoneX) // apply smoothing to the line

// 8. An array of objects of length N. Each object has key -> value pair, the key being "y" and the value is a random number
var dataset = d3.range(n).map(function(d) { return {"y": d3.randomUniform(1)() } })

// 1. Add the SVG to the page and employ #2
var svg = d3.select("#viz").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// 3. Call the x axis in a group tag
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

// 4. Call the y axis in a group tag
svg.append("g")
    .attr("class", "y axis")
    .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

// 9. Append the path, bind the data, and call the line generator 
svg.append("path")
    .datum(dataset) // 10. Binds data to the line 
    .attr("class", "line") // Assign a class for styling 
    .attr("d", line); // 11. Calls the line generator 
