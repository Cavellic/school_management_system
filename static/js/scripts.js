var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

function openSidebar() {
    if (!sidebarOpen) {
        sidebar.classList.add("sidebar-responsive");
        sidebarOpen = true;

    }
}

function closeSidebar() {
    if (sidebarOpen) {
        sidebar.classList.remove("sidebar-responsive");
        sidebarOpen = false;
    }
}

/*------Charts---------*/

/*------Pie Chart------*/
var pieChart_options = {
    series: [550, 30],
    chart: {
    width: 380,
    type: 'pie',
  },
  labels: ['Students', 'Teachers'],
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: 200
      },
      legend: {
        position: 'bottom'
      }
    }
  }]
  };

  var Piechart = new ApexCharts(document.querySelector("#admin-pie-chart"), pieChart_options);
  Piechart.render();

/*------Bar Chart______*/
var barChart_options = {
    series: [{
    data: [4, 3, 8, 7, 5, 10, 2, 11],
    name: "Assignments"
  }],
    chart: {
    type: 'bar',
    height: 380
  },
  plotOptions: {
    bar: {
      barHeight: '100%',
      distributed: true,
      vertical: true,
      dataLabels: {
        position: 'bottom'
      },
    }
  },
  colors: ['#33b2df', '#546E7A', '#d4526e', '#13d8aa', '#A5978B', '#2b908f', '#f9a3a4', '#90ee7e'
  ],
  /*dataLabels: {
    enabled: true,
    textAnchor: 'start',
    style: {
      colors: ['#fff']
    },
    formatter: function (val, opt) {
      return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
    }, 
    offsetX: 0,
    dropShadow: {
      enabled: true
    }
  }, */
  stroke: {
    width: 1,
    colors: ['#fff']
  },
  xaxis: {
    categories: ['Maths', 'Geo', 'Science', 'English', 'Physics', 'Biology', 'Chemistry',
      'Comp Science'
    ],
  },
  yaxis: {
    labels: {
      show: false
    }
  },

  title: {
      text: '',
      align: 'center',
      color: '#fff'
  },
  tooltip: {
    theme: 'dark',
    x: {
      show: false
    },
    y: {
      title: {
        formatter: function () {
          return ''
        }
      }
    }
  }
  };

  var Barchart = new ApexCharts(document.querySelector("#student-bar-chart"), barChart_options);
  Barchart.render();

  