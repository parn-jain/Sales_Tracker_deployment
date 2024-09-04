const quarterlyChart = new Chart(document.getElementById('quarterlyChart'), {
    type: 'pie',  // Chart type
    data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],  // Labels for each segment
        datasets: [{
            label: 'Quarterly Data',
            data: [20, 10, 30, 40],  // Data for each segment
            backgroundColor: [ // Custom colors for each segment

            'rgba(54, 162, 235, 0.2)', // Blue with 20% opacity
            'rgba(255, 206, 86, 0.2)', // Yellow with 20% opacity
            'rgba(75, 192, 192, 0.2)', // Green with 20% opacity
            'rgba(153, 102, 255, 0.2)'  // Purple with 20% opacity
            ],
            borderColor: [ // Border colors for each segment
                '#990000',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1 // Width of the border
        }]
    },
    options: {
        plugins: {
            legend: {
                labels: {
                    color: 'red' // Legend text color
                }
            },
            tooltip: {
                titleColor: '#990000', // Tooltip title color
                bodyColor: 'white',  // Tooltip body color
                backgroundColor: '#007d7e' // Tooltip background color
            }
        }
    }
});

