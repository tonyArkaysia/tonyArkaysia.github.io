<!DOCTYPE html>
<div id="myChart"></div>
<script type="module">
  import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

  // Data with assists
  const playersData = [
    { name: "Nikola Jokic", points: 35, assists: 22 },
    { name: "Stephen Curry", points: 31, assists: 12 },
    { name: "Giannis Antetokounmpo", points: 45, assists: 6 },
    { name: "DeAaron Fox", points: 28, assists: 8 },
    { name: "Luka Dončić", points: 35, assists: 17 },
    { name: "Kyrie Irving", points: 35, assists: 6 },
    { name: "LeBron James", points: 23, assists: 9 },
    { name: "Kevin Durant", points: 34, assists: 3 },
    // ... more players
  ];

  // Chart dimensions and margins
  const width = 800;
  const height = 400;
  const margins = { top: 20, right: 20, bottom: 30, left: 40 };

  // Scales
  const x = d3.scaleBand()
      .domain(playersData.map(d => d.name))
      .range([margins.left, width - margins.right])
      .padding(0.1);

  const y = d3.scaleLinear()
      .domain([0, d3.max(playersData, d => Math.max(d.points, d.assists))])
      .range([height - margins.bottom, margins.top]);

  // Create SVG container
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height);

  // Add x-axis
  svg.append("g")
      .attr("transform", `translate(0,${height - margins.bottom})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", ".15em")
      .attr("transform", "rotate(-65)");

  // Add y-axis
  svg.append("g")
      .attr("transform", `translate(${margins.left},0)`)
      .call(d3.axisLeft(y));

  // Draw images for points
  svg.selectAll(".point")
      .data(playersData)
      .enter().append("image")
      .attr("class", "point")
      .attr("x", d => x(d.name) + x.bandwidth() / 3 - 10)
      .attr("y", height - margins.bottom)
      .attr("width", 20)
      .attr("height", 20)
      .attr("xlink:href", "/resources/data_charts/transparent_bball.png")
      .transition()
      .duration(1000)
      .attr("y", d => y(d.points) - 10);

  // Draw images for assists
  svg.selectAll(".assist")
      .data(playersData)
      .enter().append("image")
      .attr("class", "assist")
      .attr("x", d => x(d.name) + (2 * x.bandwidth() / 3) - 10)
      .attr("y", height - margins.bottom)
      .attr("width", 30)
      .attr("height", 30)
      .attr("xlink:href", "/resources/data_charts/flame_bball.png") // Replace with the path to your assist image
      .transition()
      .duration(1000)
      .attr("y", d => y(d.assists) - 10);

  // Append the SVG element to the specified div id
  document.getElementById("myChart").appendChild(svg.node());
</script>
