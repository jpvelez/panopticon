// Initialize calendar and day rectangle dimensions.
var width = 905,
    height = 125,
    cellSize = 17; // cell size

// Create helper functions that return a date's day-of-the-week and week-of-the-year numbers.
var day = d3.time.format("%w"),
    week = d3.time.format("%U"),
    percent = d3.format(".1%"),
    format = d3.time.format("%Y-%m-%d");

// // Map daily average rank values to color scale.
var color = d3.scale.threshold()
    .domain([0.5, 0.60, 0.69, 0.78, 1.0])
    .range(d3.range(5).map(function(d) { return "q" + d + "-5"; }));

// Draw calendar.
var svg = d3.select("#otp-cal").selectAll("svg")
    .data([2012])
  .enter().append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "otp-colors")
  .append("g")
    .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");


// Draw day rectangles.
var rect = svg.selectAll(".day")
    .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
  .enter().append("rect")
    .attr("class", "day")
    .attr("width", cellSize)
    .attr("height", cellSize)
    .attr("x", function(d) { return week(d) * cellSize; })
    .attr("y", function(d) { return day(d) * cellSize; })
    .datum(format);


// Draw month path around day rectangles using monthPath() function.
svg.selectAll(".month")
    .data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
  .enter().append("path")
    .attr("class", "month")
    .attr("d", monthPath);

// Define algorithm that draws month path.
function monthPath(t0) {
  var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
      d0 = +day(t0), w0 = +week(t0),
      d1 = +day(t1), w1 = +week(t1);
  return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
      + "H" + w0 * cellSize + "V" + 7 * cellSize
      + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
      + "H" + (w1 + 1) * cellSize + "V" + 0
      + "H" + (w0 + 1) * cellSize + "Z";
}


// Select only day rectangles that have deviations. 
var deviation_rect = rect.filter(function(d) { return d in calendar_deviations; })

// Color deviation days gray to distinguish them from days off/days missing driving data. 
// Sometimes deviations and driving data overlap. Color deviations first so driving data wins.
deviation_rect.attr("class", function(d) {
    return "day gray"
    })
  .select("title")
    .text(function(d) { return d + ":" + calendar_deviations[d][1];
  });




// Select only day rectangles that have driving rank data.
var driving_otp_rect = rect.filter(function(d) { return d in calendar_driving_otp; })

// Color driving rank rectangles according to their color quintile using the color() function. 
// color() returns the name of the css class that has the appropriate background-color value for the rect.
driving_otp_rect.attr("class", function(d) { 
    return "day " + color(calendar_driving_otp[d]); 
    })
  .select("title")
    .text(function(d) { return d + ": " + calendar_driving_otp[d]; 
  });


// Generate tooltip for day rectangles.
driving_otp_rect.on("mouseover", function (d){
      otp_pct = Math.floor(calendar_driving_otp[d] * 100)
      var title_text = "<p>" + d + ": " + otp_pct + "%" + "</p>";
      var pos = $(this).offset();
       $("#tooltip").html(title_text)
          .css({top: pos.top + 20, left: pos.left + 40})
          .show();
      })
  .on("mouseout", function (d){
      $("#tooltip").hide();
      });

// Generate tooltip for day rectangles.
deviation_rect.on("mouseover", function (d){
      var title_text = "<p>" + d + ": " + calendar_deviations[d][1] + "</p>";
      var pos = $(this).offset();
       $("#tooltip").html(title_text)
          .css({top: pos.top + 20, left: pos.left + 40})
          .show();
      })
  .on("mouseout", function (d){
      $("#tooltip").hide();
      });
