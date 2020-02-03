gdata  = jQuery.parseJSON($("#data").val())
console.log(gdata)


gdata.forEach(function (arrayItem, index) {
    $("#me").append("<div class=col-sm-12 col-md-12 col-lg-12'><h2 class='text-secondary m-2' id='name'>"+ arrayItem.name +"</h2><hr><div class='row'><div class='col-md-4 col-xs-6 col-sm-6'><div id='angleGauge' style='height: 250px'></div></div><div class='row col-lg-8 col-md-8 col-sm-12' style='font-size:0.75rem '><div class='col-lg-8 col-md-12'>Progress<div class='progress'><div class='progress-bar' role='progressbar' style='width:"+arrayItem.percent+"%' aria-valuenow='"+arrayItem.percent+"%' aria-valuemin='0' aria-valuemax='100'>"+arrayItem.percent+"%</div></div></div><div class='col-lg-4 col-md-4 col-xs-1 col-sm-1 mt-2'><a href='"+arrayItem.last_urls[arrayItem.name]+"' class='btn btn-primary btn-sm'>Start <i class='fas fa-arrow-right'></i></a></div><div class='col-md-4 col-xs-6 col-sm-6 card-body card-sm'><div class='text-center bg-primary-3 text-white card-body card'>Rewards<span class='text-white'>"+arrayItem.rewards +"</span></div></div><div class='col-md-4 col-xs-6 col-sm-6 card-body card-sm'><div class='text-center bg-primary-3 text-white card-body card'>Projects<span class='text-white'>0</span></div></div><div class='col-md-4 col-xs-6 col-sm-6 card-body card-sm'><div class='text-center bg-primary-3 text-white card-body card'>Quizzes<span class='text-white'>"+arrayItem.quizes+"/"+arrayItem.topics+"</span></div></div></div></div><div id='activeCourseMCQ"+index+"' class='border rounded shadow-3d'></div><!-- <hr> --><div id='activeCoursePS"+index+"' class='border rounded shadow-3d mt-3'></div></div></div>")

Highcharts.chart('activeCourseMCQ'+index, {
    chart: {
        type: 'column',
        scrollablePlotArea: {
            minWidth: 3700,
            scrollPositionX: 1
        }
    },
    title: {
        text: 'Quiz Performance'
    },
    xAxis: {
        categories: arrayItem.final_test_data.tests
    },
    labels: {
        items: [{
            html: 'You vs Other members',
            style: {
                left: '50px',
                top: '18px',
                color: ( // theme
                    Highcharts.defaultOptions.title.style &&
                    Highcharts.defaultOptions.title.style.color
                ) || 'black'
            }
        }]
    },
    series: [{
        type: 'column',
        name: arrayItem.final_test_data.user5.name,
        data: arrayItem.final_test_data.user5.data
    },{
        type: 'column',
        name: arrayItem.final_test_data.user4.name,
        data: arrayItem.final_test_data.user4.data
    },{
        type: 'column',
        name: arrayItem.final_test_data.user3.name,
        data: arrayItem.final_test_data.user3.data
    }, {
        type: 'column',
        name: arrayItem.final_test_data.user2.name,
        data: arrayItem.final_test_data.user2.data
    }, {
        type: 'column',
        name: arrayItem.final_test_data.user1.name,
        data: arrayItem.final_test_data.user1.data
    }]
});





// Highcharts.chart('activeCoursePS'+index, {
//     chart: {
//         type: 'column',
//         height:250,
//         scrollablePlotArea: {
//             minWidth: 700,
//             scrollPositionX: 1
//         }
//     },
//     title: {
//         text: 'Problem solving skills'
//     },
//     xAxis: {
//         categories: arrayItem.final_assignment_data.chapters
//     },
//     labels: {
//         items: [{
//             html: 'You vs Other members',
//             style: {
//                 left: '50px',
//                 top: '18px',
//                 color: ( // theme
//                     Highcharts.defaultOptions.title.style &&
//                     Highcharts.defaultOptions.title.style.color
//                 ) || 'black'
//             }
//         }]
//     },
//     series: [
//     {
//         type: 'column',
//         name: arrayItem.final_assignment_data.user1.name,
//         data: arrayItem.final_assignment_data.user1.data
//     },
//     {
//         type: 'column',
//         name: arrayItem.final_assignment_data.user2.name,
//         data: arrayItem.final_assignment_data.user2.data
//     },
//     {
//         type: 'column',
//         name: arrayItem.final_assignment_data.user3.name,
//         data: arrayItem.final_assignment_data.user3.data
//     },
//     {
//         type: 'column',
//         name: arrayItem.final_assignment_data.user4.name,
//         data: arrayItem.final_assignment_data.user4.data
//     },
//     {
//         type: 'column',
//         name: arrayItem.final_assignment_data.user5.name,
//         data: arrayItem.final_assignment_data.user5.data
//     }
//     ]
// });


Highcharts.chart('activeCoursePS'+index, {
    chart: {
        type: 'column',
        scrollablePlotArea: {
            minWidth: 3700,
            scrollPositionX: 1
        }
    },
    title: {
        text: 'Problem solving skills vs time'
    },
    xAxis: {
        categories: arrayItem.final_assignment_data.chapters
    },
    yAxis: [{
        min: 0,
        title: {
            text: 'Problems Solved'
        }
    }, {
        title: {
            text: 'Time -> no of units * 15mins'
        },
        opposite: true
    }],
    legend: {
        shadow: false
    },
    tooltip: {
        shared: true
    },
    plotOptions: {
        column: {
            grouping: true,
            shadow: true,
            borderWidth: 0
        }
    },
    series: [{
        name: arrayItem.final_assignment_data.user1.name,
        color: 'red',
        data: arrayItem.final_assignment_data.user1.data,
        pointPadding: 0.3,
        pointPlacement: -0.2
    }, {
        showInLegend: false,
        color: 'rgba(126,86,134,.9)',
        data: arrayItem.final_assignment_data.user1.time,
        pointPadding: 0.4,
        pointPlacement: -0.2
    },{
        name: arrayItem.final_assignment_data.user2.name,
        color: 'blue',
        data: arrayItem.final_assignment_data.user2.data,
        pointPadding: 0.3,
        pointPlacement: -0.2
    }, {
        showInLegend: false,
        color: 'rgba(126,86,134,.9)',
        data: arrayItem.final_assignment_data.user2.time,
        pointPadding: 0.4,
        pointPlacement: -0.2
    },{
        name: arrayItem.final_assignment_data.user3.name,
        color: 'green',
        data: arrayItem.final_assignment_data.user3.name,
        pointPadding: 0.3,
        pointPlacement: -0.2
    }, {
        showInLegend: false,
        color: 'rgba(126,86,134,.9)',
        data: arrayItem.final_assignment_data.user3.time,
        pointPadding: 0.4,
        pointPlacement: -0.2
    },{
        name: arrayItem.final_assignment_data.user4.name,
        color: 'black',
        data: arrayItem.final_assignment_data.user4.data,
        pointPadding: 0.3,
        pointPlacement: -0.2
    }, {
        showInLegend: false,
        color: 'rgba(126,86,134,.9)',
        data: arrayItem.final_assignment_data.user4.time,
        pointPadding: 0.4,
        pointPlacement: -0.2
    },{
        name: arrayItem.final_assignment_data.user5.name,
        color: 'yellow',
        data: arrayItem.final_assignment_data.user5.data,
        pointPadding: 0.3,
        pointPlacement: -0.2
    }, {
        name: "timetaken",
        color: 'rgba(126,86,134,.9)',
        data: arrayItem.final_assignment_data.user5.time,
        pointPadding: 0.4,
        pointPlacement: -0.2
    }]
});
});


Highcharts.chart('angleGauge', {

    chart: {
        type: 'gauge',
        plotBackgroundColor: null,
        plotBackgroundImage: null,
        plotBorderWidth: 0,
        plotShadow: false
    },

    title: {
        text: 'Angle'
    },

    pane: {
        startAngle: -150,
        endAngle: 150,
        background: [{
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#FFF'],
                    [1, '#333']
                ]
            },
            borderWidth: 0,
            outerRadius: '109%'
        }, {
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#333'],
                    [1, '#FFF']
                ]
            },
            borderWidth: 2,
            outerRadius: '107%'
        }, {
            // default background
        }, {
            backgroundColor: '#DDD',
            borderWidth: 0,
            outerRadius: '105%',
            innerRadius: '103%'
        }]
    },

    // the value axis
    yAxis: {
        min: -90,
        max: 90,

        minorTickInterval: 'auto',
        minorTickWidth: 1,
        minorTickLength: 10,
        minorTickPosition: 'inside',
        minorTickColor: '#666',

        tickPixelInterval: 10,
        tickWidth: 2,
        tickPosition: 'inside',
        tickLength: 10,
        tickColor: '#666',
        labels: {
            step: 2,
            rotation: 'auto'
        },
        title: {
            text: 'degrees'
        },
        plotBands:
        [{
          innerRadius: '50%',
          outerRadius: '100%'
          },{
            from: 30,
            to: 90,
            color: '#DF5353' // green
        },{
            from: -30,
            to: 30,
            color: 'green' // green
        },  {
            from: -90,
            to: -30,
            color: '#DF5353' // red
        }]
    },

    series: [{
        name: 'Speed',
        data: [0],
        tooltip: {
            valueSuffix: ' o degrees'
        }
    }]

},
// Add some life
);



function getPointCategoryName(point, dimension) {
    var series = point.series,
        isY = dimension === 'y',
        axis = series[isY ? 'yAxis' : 'xAxis'];
    return axis.categories[point[isY ? 'y' : 'x']];
}

// Highcharts.chart('heatDraw', {

//     chart: {
//         type: 'heatmap',
//         marginTop: 40,
//         marginBottom: 80,
//         plotBorderWidth: 1
//     },


//     title: {
//         text: 'Topic wise performance'
//     },

//     xAxis: {
//         categories: ['Topic 1', 'Topic 2', 'Topic 3', 'Topic 4', 'Topic 5', 'Topic 6', 'Topic 7', 'Topic 8', 'Topic 9', 'Topic 10']
//     },

//     yAxis: {
//         categories: ['Chapt 1', 'Chapt 2', 'Chapt 3', 'Chapt 4', 'Chapt 5'],
//         title: null,
//         reversed: true
//     },

//     accessibility: {
//         point: {
//             descriptionFormatter: function (point) {
//                 var ix = point.index + 1,
//                     xName = getPointCategoryName(point, 'x'),
//                     yName = getPointCategoryName(point, 'y'),
//                     val = point.value;
//                 return ix + '. ' + xName + ' sales ' + yName + ', ' + val + '.';
//             }
//         }
//     },

//     colorAxis: {
//         min: 0,
//         minColor: '#FFFFFF',
//         maxColor: Highcharts.getOptions().colors[0]
//     },

//     legend: {
//         align: 'right',
//         layout: 'vertical',
//         margin: 0,
//         verticalAlign: 'top',
//         y: 25,
//         symbolHeight: 280
//     },

//     tooltip: {
//         formatter: function () {
//             return '<b>' + this.point.value + '</b> points in <br><b>"' + getPointCategoryName(this.point, 'x') +'"</b>  of <br><b>' + getPointCategoryName(this.point, 'y') + '</b>';
//         }
//     },

//     series: [{
//         name: 'Topics wise progress',
//         borderWidth: 1,
//         data: [[0, 0, 10], [0, 1, 19], [0, 2, 8], [0, 3, 24], [0, 4, 67], [1, 0, 92], [1, 1, 58], [1, 2, 78], [1, 3, 117], [1, 4, 48], [2, 0, 35], [2, 1, 15], [2, 2, 123], [2, 3, 64], [2, 4, 52], [3, 0, 72], [3, 1, 132], [3, 2, 114], [3, 3, 19], [3, 4, 16], [4, 0, 38], [4, 1, 5], [4, 2, 8], [4, 3, 117], [4, 4, 115], [5, 0, 88], [5, 1, 32], [5, 2, 12], [5, 3, 6], [5, 4, 120], [6, 0, 13], [6, 1, 44], [6, 2, 88], [6, 3, 98], [6, 4, 96], [7, 0, 31], [7, 1, 1], [7, 2, 82], [7, 3, 32], [7, 4, 30], [8, 0, 85], [8, 1, 97], [8, 2, 123], [8, 3, 64], [8, 4, 84], [9, 0, 47], [9, 1, 114], [9, 2, 31], [9, 3, 48], [9, 4, 91]],
//         dataLabels: {
//             enabled: true,
//             color: '#000000'
//         }
//     }],

//     responsive: {
//         rules: [{
//             condition: {
//                 maxWidth: 500
//             },
//             chartOptions: {
//                 yAxis: {
//                     labels: {
//                         formatter: function () {
//                             return this.value.charAt(0);
//                         }
//                     }
//                 }
//             }
//         }]
//     }

// });