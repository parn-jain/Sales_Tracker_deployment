



 $(document).ready(function() {
  $(".hamburger").click(function() {
    $(".stick").each(function() {
      if ($(this).hasClass('open')) {
        $(this).removeClass('open').addClass('close');
      } else {
        $(this).removeClass('close').addClass('open');
      }
    });
  });
});





// Weekly Data Chart
var ctxWeekly = document.getElementById('weeklyChart').getContext('2d');
var weeklyChart = new Chart(ctxWeekly, {
    type: 'doughnut',
    data: {
        labels: ['Completed', 'Remaining'],
        datasets: [{
            label: 'Weekly Data',
            data: [parseInt('{{ mining_count }}', 10), 40 - parseInt('{{ mining_count }}', 10)],
            backgroundColor: ['#4CAF50', '#e0e0e0'],
            borderColor: ['#33CC33', '#e0e0e0'],
            borderWidth: 1
        }]
    },
    options: {
        cutout: '70%',
        plugins: {
            legend: {
                labels: {
                    color: '#1f1d1c', // Font color for the legend
                    font: {
                        size: 14, // Font size for the legend
                    }
                }
            }
        }
    }
});

// Monthly Data Chart
var ctxMonthly = document.getElementById('monthlyChart').getContext('2d');
var monthlyChart = new Chart(ctxMonthly, {
    type: 'doughnut',
    data: {
        labels: ['Completed', 'Remaining'],
        datasets: [{
            label: 'Monthly Data',
            data: [parseInt('{{ mining_count }}', 10), 100 - parseInt('{{ mining_count }}', 10)],
           backgroundColor: ['#4CAF50', '#e0e0e0'],
            borderColor: ['#4CAF50', '#e0e0e0'],
            borderWidth: 1
        }]
    },
    options: {
        cutout: '70%',
        plugins: {
            legend: {
                labels: {
                    color: '#1f1d1c', // Font color for the legend
                    font: {
                        size: 14, // Font size for the legend
                    }
                }
            }
        }
    }
});

// Quarterly Data Chart
var ctxQuarterly = document.getElementById('quarterlyChart').getContext('2d');
var quarterlyChart = new Chart(ctxQuarterly, {
    type: 'doughnut',
    data: {
        labels: ['Completed', 'Remaining'],
        datasets: [{
            label: 'Quarterly Data',
            data: [parseInt('{{ mining_count }}', 10), 300 - parseInt('{{ mining_count }}', 10)],
            backgroundColor: ['#4CAF50', '#e0e0e0'],
            borderColor: ['#4CAF50', '#e0e0e0'],
            borderWidth: 1
        }]
    },
    options: {
        cutout: '70%',
        plugins: {
            legend: {
                labels: {
                    color: '#1f1d1c', // Font color for the legend
                    font: {
                        size: 14, // Font size for the legend
                    }
                }
            }
        }
    }
});





/**clickable */
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.nav-link.dropdown-toggle').forEach(function (toggle) {
        toggle.addEventListener('click', function (event) {
            event.preventDefault();
            const menu = this.nextElementSibling;

            document.querySelectorAll('.dropdown-menu').forEach(function (item) {
                if (item !== menu) {
                    item.classList.remove('show');
                }
            });

            menu.classList.toggle('show');
        });
    });

    document.addEventListener('click', function (event) {
        document.querySelectorAll('.dropdown-menu').forEach(function (menu) {
            if (!menu.contains(event.target) && !menu.previousElementSibling.contains(event.target)) {
                menu.classList.remove('show');
            }
        });
    });
});


function toggleNavbar() {
    const navbar = document.querySelector('.nav-links');
    navbar.style.display = navbar.style.display === 'block' ? 'none' : 'block';
  }