import { useNavigate } from 'react-router-dom'

function SearchFilters() {
  const navigate = useNavigate()

  return (
    <div className="search-filters">
      <input
        type="text"
        placeholder="Поиск..."
        className="search-input"
      />
      <div className="filters">
        <select className="filter-select">
          <option>Дата ▼</option>
        </select>
        <select className="filter-select">
          <option>Тип ошибки ▼</option>
        </select>
        <select className="filter-select">
          <option>Статус ▼</option>
        </select>
      </div>
      <button
        className="btn-upload"
        onClick={() => navigate('/upload')}
      >
        + Новый анализ
      </button>
    </div>
  )
}

export default SearchFilters