<?php
  include_once("php/connect.php");

  $forecastHours = 24;
  $query = "SELECT * FROM (SELECT * FROM Predictions ORDER BY datetime_GMT DESC LIMIT " . strval($forecastHours) . ") sub ORDER BY datetime_GMT ASC";

  if (!$result = mysqli_query($con, $query)) {
    echo "Problem getting predictions.<br>";
    echo mysqli_error($con) . "<br>";
  }

  $predictions = array();
  while ($prediction = mysqli_fetch_assoc($result))
    $predictions[] = $prediction;

  $jsonString = "{\"chart_data\":[";
  $numberOfJSONObjects = count($predictions);
  for ($index = 0; $index < $numberOfJSONObjects; $index++) {
    $currentDatetime = $predictions[$index]['datetime_GMT'];
    $currentPrediction = 0.0;
    if ($predictions[$index]['generation_MW'] > 0.0)
      $currentPrediction = $predictions[$index]['generation_MW'];

    $jsonString .= "{\"Date\":\"" . strval($currentDatetime) . "\",\"Label\":" . strval($currentPrediction) . "}";
    if ($index < $numberOfJSONObjects - 1)
      $jsonString .= ",";
  }

  $jsonString .= "]}";
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>PV Forecast Manchester</title>
    <script src="https://d3js.org/d3.v4.min.js"></script>
    <link rel="stylesheet" type="text/css" href="http://www.pvforecastmanchester.xyz/css/stylesheet.css">
    <link rel="shortcut icon" href="http://www.pvforecastmanchester.xyz/favicon.ico" type="image/x-icon">
    <link rel="icon" href="http://www.pvforecastmanchester.xyz/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
  </head>

  <body>
    <h2>Greater Manchester PV Forecast</h2>
    <div id="graphDiv"></div>
    <script>
      var jsonString = '<?php echo $jsonString; ?>';
      jsonObject = JSON.parse(jsonString);
      graphData = jsonObject.chart_data;

      var margin = {top: 20, right: 100, bottom: 50, left: 70},
              width = 860 - margin.left - margin.right,
              height = 400 - margin.top - margin.bottom;

      var parseDate = d3.timeParse("%Y-%m-%d %H:%M:%S");

      var x = d3.scaleTime().range([0, width]);
      var y = d3.scaleLinear().range([height, 0]);

      var label = d3.line()
        .x(function(d) { return x(d.Date); })
        .y(function(d) { return y(d.Label); });

      var svg = d3.select("#graphDiv")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");


      function drawGraph(data) {
        data.forEach(function(d) {
          d.Date = parseDate(d.Date);
          d.Label = +d.Label;
        });

        data.sort(function(a, b) {
          return a["Date"] - b["Date"];
        })

        x.domain(d3.extent(data, function(d) { return d.Date; }));
        y.domain([0, d3.max(data, function(d) { return d.Label; })]);

        svg.append("path")
          .data([data])
          .style("stroke", "#660099")
          .attr("class", "line")
          .attr("d", label(data));

        svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));

        svg.append("text")             
          .attr("transform",
                "translate(" + (width / 2) + "," + (height + margin.top + 20) + ")")
          .style("text-anchor", "middle")
          .text("Date");

        svg.append("g")
          .call(d3.axisLeft(y));

        svg.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - margin.left)
          .attr("x",0 - (height / 2))
          .attr("dy", "1em")
          .style("text-anchor", "middle")
          .text("Expected PV Generation (MW)");
      }

      drawGraph(graphData);
    </script>
  </body>
</html>