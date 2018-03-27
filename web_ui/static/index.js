function fitToContainer(canvas){
  // Make it visually fill the positioned parent
  canvas.style.width ='100%';
  canvas.style.height='100%';
  // ...then set the internal size to match
  canvas.width  = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
}

function myYRangeFunction(range) {
  var min = range.min - 3;
  var max = range.max + 3;
  return {min: min, max: max};
}

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
    isRed = roi_value < 0;
    if (isRed) {
      market_color = 'red';
      badge_color = 'badge-danger';
      var red_full = "rgb(255,0,0,1)";
      var red_light = "rgb(255,0,0,0.2)";
      roi_chart["seriesSet"][0]["options"]["strokeStyle"] = red_full;
      roi_chart["seriesSet"][0]["options"]["fillStyle"] = red_light;

      total_value_chart["seriesSet"][0]["options"]["strokeStyle"] = red_full;
      total_value_chart["seriesSet"][0]["options"]["fillStyle"] = red_light;
    } else {
      market_color = 'green';
      badge_color = 'badge-success';

      var green_full = "rgb(0,255,0,1)";
      var green_light = "rgb(0,255,0,0.2)";
      roi_chart["seriesSet"][0]["options"]["strokeStyle"] = green_full;
      roi_chart["seriesSet"][0]["options"]["fillStyle"] = green_light;

      total_value_chart["seriesSet"][0]["options"]["strokeStyle"] = green_full;
      total_value_chart["seriesSet"][0]["options"]["fillStyle"] = green_light;
    }

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

// And for a doughnut chart
data = {
    datasets: [{
        data: [],
        backgroundColor: colors,
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
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
  total_value_chart = new SmoothieChart({millisPerPixel:100,tooltip:true,yRangeFunction:myYRangeFunction});
  total_value_cv = document.getElementById('current_total_value');
  fitToContainer(total_value_cv);
  total_value_chart.addTimeSeries(total_values, { strokeStyle: 'rgba(0, 255, 0, 1)', fillStyle: 'rgba(0, 255, 0, 0.2)', lineWidth: 2 });
  total_value_chart.streamTo(total_value_cv, 500);

  roi_values = new TimeSeries();
  roi_chart = new SmoothieChart({millisPerPixel:100,tooltip:true,yRangeFunction:myYRangeFunction});
  roi_cv = document.getElementById('roi_value');
  fitToContainer(roi_cv);
  roi_chart.addTimeSeries(roi_values, { strokeStyle: 'rgba(0, 255, 0, 1)', fillStyle: 'rgba(0, 255, 0, 0.2)', lineWidth: 2 });
  roi_chart.streamTo(roi_cv, 500);
});

socket.on('state_update', update_state);
});
