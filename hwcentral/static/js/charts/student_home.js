// Code to Run Google Charts API

// Student Home Over View Chart
                google.load("visualization", "1", {packages:["corechart"]});
                google.setOnLoadCallback(drawChart);
                function drawChart() {
                    var data = google.visualization.arrayToDataTable([
                        ['Subject', 'Your Score', 'Class Average'],
                        ['Maths', 90, 70],
                        ['English', 70, 46],
                        ['Science', 60, 96],
                        ['History', 80, 76],
                        ['Geography', 70, 46],
                        ['Economics', 60, 96]
                    ]);

                    var options = {
                        legend: { position: "top" },
                        backgroundColor: { fill: 'transparent' },
                        hAxis: {
                            gridlines: {
                                color: 'transparent'
                            }
                        }
                    };

                    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));

                    chart.draw(data, options);
                }



