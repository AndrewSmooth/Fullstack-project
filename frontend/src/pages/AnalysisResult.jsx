import { useParams, useNavigate } from 'react-router-dom'

function AnalysisResult() {
  const { id } = useParams()
  const navigate = useNavigate()

  // Моковые данные (в реальности будут приходить с бэкенда)
  const analysisData = {
    pipeline: 'main-pipeline-build',
    status: 'Ошибка найдена',
    classification: 'Dependency Conflict',
    confidence: '92%',
    analysisTime: '3.2с',
    logFragment: `[INFO] Installing dependencies...
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
npm ERR! While resolving: project@1.0.0
npm ERR! Found: react@18.2.0
npm ERR! node_modules/react`,
    aiRecommendation: {
      reason: 'Конфликт версий зависимостей между react@18.2.0 и требуемой версией',
      steps: [
        'Обновить package.json',
        'Запустить npm install --legacy-peer-deps',
        'Пересобрать проект'
      ],
      similarCases: 3
    }
  }

  return (
    <div className="result-page">
      {/* Хлебные крошки */}
      <nav className="breadcrumbs">
        <span className="breadcrumb-item" onClick={() => navigate('/')}>Главная</span>
        <span className="breadcrumb-separator">&gt;</span>
        <span className="breadcrumb-item" onClick={() => navigate('/catalog')}>Анализы</span>
        <span className="breadcrumb-separator">&gt;</span>
        <span className="breadcrumb-item active">{analysisData.pipeline}</span>
      </nav>

      {/* Информационная панель */}
      <div className="info-panel">
        <div className="info-block">
          <div className="info-label">Статус:</div>
          <div className="info-value">{analysisData.status}</div>
        </div>
        <div className="info-block">
          <div className="info-label">Классификация:</div>
          <div className="info-value">{analysisData.classification}</div>
        </div>
        <div className="info-block">
          <div className="info-label">Уверенность AI:</div>
          <div className="info-value">{analysisData.confidence}</div>
        </div>
        <div className="info-block">
          <div className="info-label">Время анализа:</div>
          <div className="info-value">{analysisData.analysisTime}</div>
        </div>
      </div>

      {/* Основная часть: лог и рекомендации */}
      <div className="result-content">
        {/* Фрагмент лога */}
        <div className="log-section">
          <h3 className="section-title">Фрагмент лога:</h3>
          <pre className="log-content">
            <code>{analysisData.logFragment}</code>
          </pre>
        </div>

        {/* Рекомендации AI */}
        <div className="ai-section">
          <h3 className="section-title">Рекомендация AI</h3>

          <div className="ai-recommendation">
            <div className="ai-block">
              <strong>Причина:</strong>
              <p>{analysisData.aiRecommendation.reason}</p>
            </div>

            <div className="ai-block">
              <strong>Пошаговое решение:</strong>
              <ol className="solution-steps">
                {analysisData.aiRecommendation.steps.map((step, index) => (
                  <li key={index}>{step}</li>
                ))}
              </ol>
            </div>

            <div className="ai-block">
              <strong>Похожие случаи:</strong>
              <p>{analysisData.aiRecommendation.similarCases} похожих ошибки найдено в истории</p>
            </div>

            <div className="ai-actions">
              <button className="btn-action">Скопировать фикс</button>
              <button className="btn-action">Экспорт в отчёт</button>
            </div>
          </div>
        </div>
      </div>

      {/* Заметки разработчика */}
      <div className="notes-section">
        <h3 className="section-title">Заметки разработчика:</h3>
        <textarea
          className="notes-textarea"
          placeholder="Введите заметки..."
          rows="4"
        />
        <button className="btn-save">Сохранить</button>
      </div>
    </div>
  )
}

export default AnalysisResult