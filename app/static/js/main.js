// Main JavaScript for Score Ambiental

document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Password visibility toggle
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            }
        });
    });

    // Handle activity logging
    const activityForm = document.getElementById('activityForm');
    if (activityForm) {
        activityForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(activityForm);
            const activityData = {
                activity_type: formData.get('activity_type'),
                description: formData.get('description'),
                points: parseFloat(formData.get('points'))
            };
            
            fetch('/log-activity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(activityData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Show success message
                    const toast = new bootstrap.Toast(document.getElementById('activityToast'));
                    toast.show();
                    
                    // Update UI
                    if (data.total_score !== undefined) {
                        const scoreElement = document.querySelector('.total-score');
                        if (scoreElement) {
                            scoreElement.textContent = Math.round(data.total_score);
                        }
                    }
                    
                    // Reset form
                    activityForm.reset();
                    
                    // Close modal if open
                    const modal = bootstrap.Modal.getInstance(document.getElementById('logActivityModal'));
                    if (modal) {
                        modal.hide();
                    }
                    
                    // Reload the page to show updated activities
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                } else {
                    throw new Error(data.message || 'Erro ao salvar atividade');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocorreu um erro ao salvar a atividade. Por favor, tente novamente.');
            });
        });
    }

    // Initialize charts if on dashboard
    if (document.getElementById('scoreChart')) {
        initializeScoreChart();
    }
});

// Initialize score chart
function initializeScoreChart() {
    const ctx = document.getElementById('scoreChart').getContext('2d');
    const chartData = JSON.parse(document.getElementById('chartData').textContent);
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Água', 'Energia', 'Mobilidade', 'Alimentação', 'Resíduos', 'Bem-estar'],
            datasets: [{
                label: 'Seu Desempenho',
                data: [
                    chartData.water_score || 0,
                    chartData.energy_score || 0,
                    chartData.mobility_score || 0,
                    chartData.food_score || 0,
                    chartData.waste_score || 0,
                    chartData.wellbeing_score || 0
                ],
                backgroundColor: 'rgba(25, 135, 84, 0.2)',
                borderColor: 'rgba(25, 135, 84, 1)',
                pointBackgroundColor: 'rgba(25, 135, 84, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(25, 135, 84, 1)'
            }]
        },
        options: {
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: {
                        stepSize: 20
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.raw} pontos`;
                        }
                    }
                }
            }
        }
    });
}

// Handle dark mode toggle
function toggleDarkMode() {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-bs-theme') === 'dark';
    
    if (isDark) {
        html.removeAttribute('data-bs-theme');
        localStorage.setItem('theme', 'light');
    } else {
        html.setAttribute('data-bs-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    }
    
    // Update icon
    const icon = document.querySelector('.theme-toggle i');
    if (icon) {
        icon.className = isDark ? 'bi bi-moon' : 'bi bi-sun';
    }
}

// Check for saved theme preference
function checkThemePreference() {
    const theme = localStorage.getItem('theme') || 'light';
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-bs-theme', 'dark');
    }
    
    // Set correct icon
    const icon = document.querySelector('.theme-toggle i');
    if (icon) {
        icon.className = theme === 'dark' ? 'bi bi-sun' : 'bi bi-moon';
    }
}

// Initialize theme
checkThemePreference();
