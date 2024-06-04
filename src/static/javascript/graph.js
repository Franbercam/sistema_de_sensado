document.addEventListener('DOMContentLoaded', function () {
    const labels = JSON.parse(document.getElementById('chart-data').dataset.labels);
    const temperatures = JSON.parse(document.getElementById('chart-data').dataset.temperatures);
    const humidities = JSON.parse(document.getElementById('chart-data').dataset.humidities);

    // Gráfica de Temperatura
    const ctxTemp = document.getElementById('temperatureChart').getContext('2d');
    const temperatureChart = new Chart(ctxTemp, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Temperatura (°C)',
                data: temperatures,
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute'
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Gráfica de Humedad
    const ctxHum = document.getElementById('humidityChart').getContext('2d');
    const humidityChart = new Chart(ctxHum, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Humedad (%)',
                data: humidities,
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute'
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
