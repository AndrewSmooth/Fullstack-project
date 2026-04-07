function Analytics() {
  return (
    <div className="analytics-page">
      {/* Заголовок + выбор даты */}
      <div className="analytics-header">
        <h2 className="page-title-large">Аналитика ошибок за неделю</h2>
        <select className="date-select">
          <option>1-7 апреля 2026 ▼</option>
        </select>
      </div>

      {/* KPI Карточки */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <span className="kpi-label">Всего сбоев</span>
          <span className="kpi-value">47</span>
        </div>
        <div className="kpi-card">
          <span className="kpi-label">Доминирующий тип</span>
          <span className="kpi-value">Permission</span>
        </div>
      </div>

      {/* Распределение по категориям */}
      <div className="chart-card">
        <h3 className="chart-title">Распределение по категориям</h3>
        <div className="category-chart">
          <div className="bar-wrapper" style={{ width: '40%' }}><span>Permission 40%</span></div>
          <div className="bar-wrapper" style={{ width: '25%' }}><span>Dependency 25%</span></div>
          <div className="bar-wrapper" style={{ width: '20%' }}><span>Timeout 20%</span></div>
          <div className="bar-wrapper" style={{ width: '10%' }}><span>Syntax 10%</span></div>
          <div className="bar-wrapper" style={{ width: '7%' }}><span>Other 5%</span></div>
        </div>
      </div>

      {/* Динамика по дням */}
      <div className="chart-card">
        <h3 className="chart-title">Динамика сбоев по дням (Пн-Вс)</h3>
        <div className="line-chart-wrap">
          <svg viewBox="0 0 600 120" className="line-chart">
            <polyline
              points="30,90 100,60 170,100 240,40 310,70 380,50 450,80 520,60"
              fill="none"
              stroke="#000"
              strokeWidth="2"
            />
            <circle cx="30" cy="90" r="4" fill="#000" />
            <circle cx="100" cy="60" r="4" fill="#000" />
            <circle cx="170" cy="100" r="4" fill="#000" />
            <circle cx="240" cy="40" r="4" fill="#000" />
            <circle cx="310" cy="70" r="4" fill="#000" />
            <circle cx="380" cy="50" r="4" fill="#000" />
            <circle cx="450" cy="80" r="4" fill="#000" />
            <circle cx="520" cy="60" r="4" fill="#000" />
          </svg>
          <div className="x-labels">
            <span>Пн</span><span>Вт</span><span>Ср</span><span>Чт</span><span>Пт</span><span>Сб</span><span>Вс</span>
          </div>
        </div>
      </div>

      {/* Топ проблем */}
      <div className="table-card">
        <h3 className="chart-title">Топ-повторяющиеся проблемы</h3>
        <table className="analytics-table">
          <thead>
            <tr>
              <th>Ошибка</th>
              <th>Количество случаев</th>
              <th>Рекомендованное действие</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Permission denied</td>
              <td>19</td>
              <td>Провести аудит Docker-образов</td>
            </tr>
            <tr>
              <td>Dependency conflict</td>
              <td>12</td>
              <td>Обновить package.json</td>
            </tr>
            <tr>
              <td>Timeout after 300s</td>
              <td>9</td>
              <td>Оптимизировать скрипты</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Кнопки действий */}
      <div className="analytics-actions">
        <button className="btn-primary">Скачать PDF</button>
      </div>
    </div>
  )
}

export default Analytics