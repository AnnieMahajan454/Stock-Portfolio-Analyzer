// Portfolio Dashboard JavaScript

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

function initDashboard() {
    const data = portfolioData;
    
    // Update KPIs
    document.getElementById('totalValueKPI').textContent = '$' + data.total_value.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('investedKPI').textContent = '$' + data.total_invested.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('gainKPI').textContent = '$' + data.total_gain.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('gainPctKPI').textContent = '+' + data.total_return_pct.toFixed(2) + '%';
    document.getElementById('sharpeKPI').textContent = data.sharpe_ratio.toFixed(2);
    
    document.getElementById('volatilityKPI').textContent = (data.annual_volatility * 100).toFixed(1) + '%';
    document.getElementById('sharpe2KPI').textContent = data.sharpe_ratio.toFixed(2);
    document.getElementById('drawdownKPI').textContent = (data.max_drawdown * 100).toFixed(1) + '%';
    document.getElementById('returnKPI').textContent = '+' + data.total_return_pct.toFixed(2) + '%';
    
    // Populate holdings table
    const holdingsBody = document.querySelector('#holdingsTable tbody');
    data.holdings.forEach(h => {
        const row = holdingsBody.insertRow();
        const gainLossClass = h.gain_loss_pct >= 0 ? 'positive' : 'negative';
        const sign = h.gain_loss_pct >= 0 ? '+' : '';
        row.innerHTML = `
            <td><span class="ticker">${h.ticker}</span></td>
            <td>${h.company}</td>
            <td>${h.shares}</td>
            <td>$${h.purchase_price.toFixed(2)}</td>
            <td>$${h.current_price.toFixed(2)}</td>
            <td>$${h.current_value.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
            <td class="${gainLossClass}">$${h.gain_loss.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
            <td class="${gainLossClass}">${sign}${h.gain_loss_pct.toFixed(2)}%</td>
        `;
    });
    
    // Populate transactions table
    const transBody = document.querySelector('#transactionsTable tbody');
    data.transactions.forEach(t => {
        const row = transBody.insertRow();
        const actionClass = t.action === 'BUY' ? 'action-buy' : 'action-sell';
        row.innerHTML = `
            <td>${t.date}</td>
            <td><span class="ticker">${t.ticker}</span></td>
            <td><span class="${actionClass}">${t.action}</span></td>
            <td>${t.shares}</td>
            <td>$${t.price.toFixed(2)}</td>
            <td>$${t.total.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
        `;
    });
    
    // Initialize charts
    initCharts(data);
}

function initCharts(data) {
    Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto";
    Chart.defaults.color = '#7f8c8d';
    Chart.defaults.borderColor = '#e0e6ed';
    
    const colors = {
        primary: '#1a73e8',
        success: '#27ae60',
        danger: '#e74c3c',
        warning: '#f39c12',
        secondary: '#34495e'
    };
    
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'bottom',
                labels: { padding: 15, font: { size: 12, weight: '500' }, color: '#2c3e50' }
            },
            tooltip: {
                backgroundColor: 'rgba(44, 62, 80, 0.9)',
                padding: 12,
                titleFont: { size: 13, weight: '600' },
                bodyFont: { size: 12 },
                borderColor: '#1a73e8',
                borderWidth: 1
            }
        }
    };
    
    // Allocation Chart
    new Chart(document.getElementById('allocationChart'), {
        type: 'doughnut',
        data: {
            labels: data.holdings.map(h => h.ticker),
            datasets: [{
                data: data.holdings.map(h => h.current_value),
                backgroundColor: ['#1a73e8', '#34495e', '#7f8c8d'],
                borderColor: 'white',
                borderWidth: 2
            }]
        },
        options: chartOptions
    });
    
    // Value Chart
    new Chart(document.getElementById('valueChart'), {
        type: 'line',
        data: {
            labels: data.metrics_history.map(m => m.date),
            datasets: [{
                label: 'Portfolio Value',
                data: data.metrics_history.map(m => m.value),
                borderColor: colors.primary,
                backgroundColor: 'rgba(26, 115, 232, 0.08)',
                tension: 0.4,
                fill: true,
                borderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 5,
                pointBackgroundColor: colors.primary
            }]
        },
        options: {...chartOptions, scales: { y: { beginAtZero: false, ticks: { color: '#7f8c8d' } }, x: { ticks: { color: '#7f8c8d' } } }}
    });
    
    // Volatility Chart
    new Chart(document.getElementById('volatilityChart'), {
        type: 'line',
        data: {
            labels: data.metrics_history.map(m => m.date),
            datasets: [{
                label: 'Volatility (%)',
                data: data.metrics_history.map(m => (m.volatility * 100).toFixed(1)),
                borderColor: colors.warning,
                backgroundColor: 'rgba(243, 156, 18, 0.08)',
                tension: 0.4,
                fill: true,
                borderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 5,
                pointBackgroundColor: colors.warning
            }]
        },
        options: {...chartOptions, scales: { y: { beginAtZero: false, ticks: { color: '#7f8c8d' } }, x: { ticks: { color: '#7f8c8d' } } }}
    });
    
    // Return Chart
    new Chart(document.getElementById('returnChart'), {
        type: 'line',
        data: {
            labels: data.metrics_history.map(m => m.date),
            datasets: [{
                label: 'Return (%)',
                data: data.metrics_history.map(m => m.return),
                borderColor: colors.success,
                backgroundColor: 'rgba(39, 174, 96, 0.08)',
                tension: 0.4,
                fill: true,
                borderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 5,
                pointBackgroundColor: colors.success
            }]
        },
        options: {...chartOptions, scales: { y: { beginAtZero: true, ticks: { color: '#7f8c8d' } }, x: { ticks: { color: '#7f8c8d' } } }}
    });
    
    // Holding Performance
    new Chart(document.getElementById('holdingPerformanceChart'), {
        type: 'bar',
        data: {
            labels: data.holdings.map(h => h.ticker),
            datasets: [{
                label: 'Return (%)',
                data: data.holdings.map(h => h.gain_loss_pct),
                backgroundColor: data.holdings.map(h => h.gain_loss_pct >= 0 ? colors.success : colors.danger),
                borderRadius: 4,
                borderSkipped: false
            }]
        },
        options: {...chartOptions, scales: { y: { beginAtZero: true, ticks: { color: '#7f8c8d' } }, x: { ticks: { color: '#7f8c8d' } } }}
    });
    
    // Sector Chart
    new Chart(document.getElementById('sectorChart'), {
        type: 'pie',
        data: {
            labels: data.holdings.map(h => h.sector),
            datasets: [{
                data: data.holdings.map(h => h.current_value),
                backgroundColor: ['#1a73e8', '#34495e', '#7f8c8d'],
                borderColor: 'white',
                borderWidth: 2
            }]
        },
        options: chartOptions
    });
    
    // Activity Chart
    const activityData = {};
    data.transactions.forEach(t => {
        const month = t.date.substring(0, 7);
        activityData[month] = (activityData[month] || 0) + 1;
    });
    
    new Chart(document.getElementById('activityChart'), {
        type: 'bar',
        data: {
            labels: Object.keys(activityData).sort(),
            datasets: [{
                label: 'Transactions',
                data: Object.values(activityData),
                backgroundColor: colors.primary,
                borderRadius: 4,
                borderSkipped: false
            }]
        },
        options: {...chartOptions, scales: { y: { beginAtZero: true, ticks: { color: '#7f8c8d' } }, x: { ticks: { color: '#7f8c8d' } } }}
    });
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', initDashboard);
