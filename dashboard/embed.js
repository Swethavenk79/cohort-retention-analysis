// Embeddable Cohort Analysis Dashboard
// Usage: Include this script in your portfolio page

(function() {
    'use strict';
    
    // Dashboard HTML template
    const dashboardHTML = `
    <style>
        .cohort-dashboard {
            --bg-primary: #0a0a0f;
            --bg-card: #1a1a24;
            --bg-elevated: #222230;
            --border: #2a2a3a;
            --text-primary: #f5f5f7;
            --text-secondary: #8b8b9a;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
            --accent-purple: #8b5cf6;
            --accent-orange: #f59e0b;
            
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--border);
        }
        
        .cohort-dashboard .header {
            padding: 24px;
            background: linear-gradient(135deg, rgba(59,130,246,0.1), transparent);
            border-bottom: 1px solid var(--border);
        }
        
        .cohort-dashboard h2 {
            margin: 0 0 8px 0;
            font-size: 20px;
            font-weight: 600;
        }
        
        .cohort-dashboard .subtitle {
            color: var(--text-secondary);
            font-size: 14px;
            margin: 0;
        }
        
        .cohort-dashboard .stats-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 16px;
            padding: 20px 24px;
            border-bottom: 1px solid var(--border);
        }
        
        .cohort-dashboard .stat {
            text-align: center;
        }
        
        .cohort-dashboard .stat-value {
            font-size: 28px;
            font-weight: 700;
            color: var(--text-primary);
        }
        
        .cohort-dashboard .stat-label {
            font-size: 12px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .cohort-dashboard .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px 24px;
        }
        
        .cohort-dashboard .chart-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
        }
        
        .cohort-dashboard .chart-title {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .cohort-dashboard .icon { font-size: 16px; }
        
        .cohort-dashboard .bar-chart {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .cohort-dashboard .bar-item {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .cohort-dashboard .bar-label {
            width: 80px;
            font-size: 12px;
            color: var(--text-secondary);
            text-transform: capitalize;
        }
        
        .cohort-dashboard .bar-track {
            flex: 1;
            height: 24px;
            background: var(--bg-elevated);
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }
        
        .cohort-dashboard .bar-fill {
            height: 100%;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 8px;
            font-size: 11px;
            font-weight: 600;
            transition: width 1s ease;
        }
        
        .cohort-dashboard .comparison-cards {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }
        
        .cohort-dashboard .comp-card {
            background: var(--bg-elevated);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }
        
        .cohort-dashboard .comp-title {
            font-size: 11px;
            color: var(--text-secondary);
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        
        .cohort-dashboard .comp-value {
            font-size: 24px;
            font-weight: 700;
        }
        
        .cohort-dashboard .comp-value.positive { color: var(--accent-green); }
        .cohort-dashboard .comp-value.negative { color: var(--accent-orange); }
        
        .cohort-dashboard .heatmap-mini {
            display: grid;
            grid-template-columns: 60px repeat(6, 1fr);
            gap: 3px;
            font-size: 10px;
        }
        
        .cohort-dashboard .heat-cell {
            aspect-ratio: 1;
            border-radius: 3px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 500;
        }
        
        .cohort-dashboard .heat-label {
            color: var(--text-secondary);
            font-size: 9px;
            display: flex;
            align-items: center;
        }
        
        .cohort-dashboard .footer {
            padding: 16px 24px;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .cohort-dashboard .btn {
            padding: 8px 16px;
            background: var(--accent-blue);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            text-decoration: none;
        }
        
        .cohort-dashboard .btn:hover {
            opacity: 0.9;
        }
    </style>
    
    <div class="cohort-dashboard">
        <div class="header">
            <h2>📊 Cohort Retention Analysis</h2>
            <p class="subtitle">3,000 users • 65K events • 18 months of data</p>
        </div>
        
        <div class="stats-row">
            <div class="stat">
                <div class="stat-value">59.7%</div>
                <div class="stat-label">Onboarding Rate</div>
            </div>
            <div class="stat">
                <div class="stat-value">35%</div>
                <div class="stat-label">Day 30 Retention</div>
            </div>
            <div class="stat">
                <div class="stat-value">$13</div>
                <div class="stat-label">Avg LTV</div>
            </div>
            <div class="stat">
                <div class="stat-value">2.1x</div>
                <div class="stat-label">Channel Variance</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-title">
                    <span class="icon">🎯</span>
                    Channel Performance (Day 30)
                </div>
                <div class="bar-chart" id="channel-bars">
                    <!-- Populated by JS -->
                </div>
            </div>
            
            <div class="chart-card">
                <div class="chart-title">
                    <span class="icon">⚡</span>
                    Onboarding Impact
                </div>
                <div class="comparison-cards">
                    <div class="comp-card">
                        <div class="comp-title">Completed</div>
                        <div class="comp-value positive">38%</div>
                        <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">Day 30 Retention</div>
                    </div>
                    <div class="comp-card">
                        <div class="comp-title">Not Completed</div>
                        <div class="comp-value negative">21%</div>
                        <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">Day 30 Retention</div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 16px; padding: 12px; background: rgba(16,185,129,0.1); border-radius: 8px;">
                    <div style="font-size: 20px; font-weight: 700; color: var(--accent-green);">+81%</div>
                    <div style="font-size: 11px; color: var(--text-secondary);">Retention Lift</div>
                </div>
            </div>
            
            <div class="chart-card" style="grid-column: 1 / -1;">
                <div class="chart-title">
                    <span class="icon">🔥</span>
                    Retention Heatmap (Sample)
                </div>
                <div class="heatmap-mini" id="heatmap-mini">
                    <!-- Populated by JS -->
                </div>
                <div style="margin-top: 12px; display: flex; align-items: center; gap: 16px; font-size: 11px; color: var(--text-secondary);">
                    <span>Low Retention</span>
                    <div style="flex: 1; height: 8px; background: linear-gradient(90deg, #ef4444, #f59e0b, #3b82f6); border-radius: 4px;"></div>
                    <span>High Retention</span>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <span>Built with Python, Pandas & Chart.js</span>
            <a href="https://github.com/Swethavenk79/cohort-retention-analysis" target="_blank" class="btn">View on GitHub →</a>
        </div>
    </div>
    `;
    
    // Data
    const channelData = [
        { name: 'organic', retention: 42, ltv: 67, color: '#10b981' },
        { name: 'referral', retention: 35, ltv: 89, color: '#8b5cf6' },
        { name: 'paid_social', retention: 28, ltv: 42, color: '#f59e0b' }
    ];
    
    const heatmapData = [
        { cohort: '2023-09', values: [100, 48, 32, 24, 18, 12] },
        { cohort: '2023-10', values: [100, 50, 34, 26, 20, 14] },
        { cohort: '2023-11', values: [100, 52, 36, 28, 22, 16] },
        { cohort: '2023-12', values: [100, 54, 38, 30, 24, 18] },
        { cohort: '2024-01', values: [100, 56, 40, 32, 26, 20] },
        { cohort: '2024-02', values: [100, 58, 42, 34, 28, 22] },
        { cohort: '2024-03', values: [100, 60, 44, 36, 30, 24] }
    ];
    
    // Render channel bars
    function renderChannelBars() {
        const container = document.getElementById('channel-bars');
        if (!container) return;
        
        const maxRetention = Math.max(...channelData.map(c => c.retention));
        
        container.innerHTML = channelData.map(channel => `
            <div class="bar-item">
                <div class="bar-label">${channel.name}</div>
                <div class="bar-track">
                    <div class="bar-fill" style="width: ${(channel.retention / maxRetention) * 100}%; background: ${channel.color};">
                        ${channel.retention}%
                    </div>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; padding-left: 92px; font-size: 11px; color: var(--text-secondary); margin-top: -8px; margin-bottom: 8px;">
                <span>$${channel.ltv} LTV</span>
                <span>${Math.round(channel.retention * 30)} users retained</span>
            </div>
        `).join('');
    }
    
    // Render mini heatmap
    function renderHeatmap() {
        const container = document.getElementById('heatmap-mini');
        if (!container) return;
        
        let html = '<div class="heat-label"></div>';
        for (let i = 0; i < 6; i++) {
            html += `<div class="heat-label">M${i}</div>`;
        }
        
        heatmapData.forEach(row => {
            html += `<div class="heat-label">${row.cohort}</div>`;
            row.values.forEach(val => {
                const hue = (val / 100) * 240;
                const lightness = 20 + (val / 100) * 20;
                const color = `hsla(${hue}, 70%, ${lightness}%, 0.9)`;
                const textColor = val > 50 ? '#fff' : '#000';
                html += `<div class="heat-cell" style="background: ${color}; color: ${textColor};">${val > 0 ? val : ''}</div>`;
            });
        });
        
        container.innerHTML = html;
    }
    
    // Initialize
    function init() {
        const container = document.getElementById('cohort-dashboard');
        if (container) {
            container.innerHTML = dashboardHTML;
            renderChannelBars();
            renderHeatmap();
        }
    }
    
    // Auto-init or manual init
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Expose for manual init
    window.CohortDashboard = { init };
})();