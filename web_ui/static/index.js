function fitToContainer(canvas){
  // Make it visually fill the positioned parent
  canvas.style.width ='100%';
  canvas.style.height='100%';
  // ...then set the internal size to match
  canvas.width  = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
}

function rangeFuncCreator(height) {
  function rangeFunction(range) {
    var min = range.min - height;
    var max = range.max + height;
    return {min: min, max: max};
  }
  return rangeFunction;
}

function makeSmoothieChart(rangeHeight, chartElementId, values) {
  var chart = new SmoothieChart({millisPerPixel:100,tooltip:true,yRangeFunction:rangeFuncCreator(3)});
  var value_cv = document.getElementById(chartElementId);
  fitToContainer(value_cv);
  chart.addTimeSeries(values, { strokeStyle: green_full, fillStyle: green_light, lineWidth: 2 });
  chart.streamTo(value_cv, 500);
  return chart;
}

var red_full = "rgb(255,0,0,1)";
var red_light = "rgb(255,0,0,0.2)";

var green_full = "rgb(0,255,0,1)";
var green_light = "rgb(0,255,0,0.2)";

function update_state(msg) {
    $('#total_amount_invested').text(msg.data["total_amount_invested"]);
    $('#total_current_value').text(msg.data["total_current_value"]);
    $('#total_current_value_2').text(msg.data["total_current_value"]);
    $('#balance').text('(' + msg.data["balance"] + ')');
    $('#balance_2').text(msg.data["balance"]);
    $('#roi').text(msg.data["roi"]);
    $('#roi_2').text(msg.data["roi"]);

    portfolio_data = msg.data["product_values"];
    myDoughnutChart.data.labels = portfolio_data["labels"];
    myDoughnutChart.data.datasets[0].data = portfolio_data["data"];
    myDoughnutChart.update();

    var total_current_value = parseFloat(msg.data["total_current_value"].substring(1));
    total_values.append(new Date().getTime(), total_current_value);

    var roi_value = parseFloat(msg.data["roi"].substring(0, msg.data["roi"].length -1));
    roi_values.append(new Date().getTime(), roi_value);

    var prev_badge = badge_color;
    var full_color = red_full;
    var light_color = red_light;

    if (roi_value < 0) {
      market_color = 'red';
      badge_color = 'badge-danger';
      full_color = red_full;
      light_color = red_light;
    } else {
      market_color = 'green';
      badge_color = 'badge-success';
      full_color = green_full;
      light_color = green_light;
    }

    roi_chart["seriesSet"][0]["options"]["strokeStyle"] = full_color;
    roi_chart["seriesSet"][0]["options"]["fillStyle"] = light_color;

    total_value_chart["seriesSet"][0]["options"]["strokeStyle"] = full_color;
    total_value_chart["seriesSet"][0]["options"]["fillStyle"] = light_color;

    $('#balance').css('color', market_color);
    $('#roi').css('color', market_color);

    $('#total_current_value_2').removeClass(prev_badge).addClass(badge_color);
    $('#balance_2').removeClass(prev_badge).addClass(badge_color);
    $('#roi_2').removeClass(prev_badge).addClass(badge_color);
}

namespace = '/state';
var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

$(document).ready(function(){
  colors = ["#041027", "#14294F","#324A76","#5B729C", "#9AACCF"];
  market_color = 'green';
  badge_color = 'badge-success';

  data = {
      datasets: [{
          data: [],
          backgroundColor: colors,
      }],
      labels: []
  };

  ctx = $('#doughnut');
  myDoughnutChart = new Chart(ctx, {
      type: 'doughnut',
      data: data,
      options: {
        tooltips: {
            enabled: true,
            mode: 'single',
            callbacks: {
                label: function (t, e) {
                  var value = e.datasets[0].data[t.index];
                  return e.labels[t.index] + ': $' + value;
                }
            }
        },
      }
  });

  socket.on('connect', function(msg) {
    total_values = new TimeSeries();
    total_value_chart = makeSmoothieChart(3, 'current_total_value', total_values);

    roi_values = new TimeSeries();
    roi_chart = makeSmoothieChart(1, 'roi_value', roi_values);
  });

  socket.on('state_update', update_state);
});
