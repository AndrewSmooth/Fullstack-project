import { useNavigate } from 'react-router-dom'

function UploadLog() {
  const navigate = useNavigate()

  return (
    <div className="upload-page">
      <h2 className="page-title-large">Загрузить лог для анализа</h2>

      {/* Зона Drag-and-Drop */}
      <div className="dropzone">
        <p>Перетащите .log / .txt файл сюда</p>
        <p className="dropzone-hint">или нажмите для выбора</p>
      </div>

      {/* Альтернативный ввод */}
      <div className="manual-input-section">
        <label className="section-label">Или вставьте содержимое лога:</label>
        <textarea
          className="log-textarea"
          placeholder="Вставьте содержимое лога здесь..."
        />
      </div>

      {/* Поля ввода */}
      <div className="form-row">
        <div className="form-group">
          <label>Название проекта:</label>
          <input type="text" defaultValue="my-project" />
        </div>
        <div className="form-group">
          <label>Ветка:</label>
          <input type="text" defaultValue="main" />
        </div>
        <div className="form-group">
          <label>Хеш коммита:</label>
          <input type="text" defaultValue="abc123def" />
        </div>
      </div>

      {/* Чекбокс */}
      <div className="checkbox-row">
        <input type="checkbox" id="auto-parse" />
        <label htmlFor="auto-parse">Использовать парсинг с gitea</label>
      </div>

      {/* Кнопка и текст поддержки */}
      <div className="actions-row">
        <button
          className="btn-primary"
          onClick={() => navigate('/analysis/mock-id')} // Переход к результату для демо
        >
          Начать анализ
        </button>
      </div>

      {/* Индикатор загрузки */}
      <div className="loading-section">
        <label className="section-label">Индикатор загрузки:</label>
        <div className="progress-bar-container">
          <div className="progress-bar-fill" style={{ width: '33%' }}></div>
        </div>
        <p className="progress-text">Анализ в процессе... 33%</p>
      </div>
    </div>
  )
}

export default UploadLog