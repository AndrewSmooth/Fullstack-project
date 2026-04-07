import { useNavigate } from 'react-router-dom'

function AnalysisTable() {
  const navigate = useNavigate()

  const analyses = [
    {
      id: 1,
      dateTime: '2026-04-01 14:32',
      pipeline: 'main/abc1231',
      status: 'process',
      errorType: 'Timeout',
    },
    {
      id: 2,
      dateTime: '2026-04-02 14:32',
      pipeline: 'main/abc1232',
      status: 'analyzed',
      errorType: 'Permission',
    },
    {
      id: 3,
      dateTime: '2026-04-03 14:32',
      pipeline: 'main/abc1233',
      status: 'process',
      errorType: 'Dependency',
    },
    {
      id: 4,
      dateTime: '2026-04-04 14:32',
      pipeline: 'main/abc1234',
      status: 'analyzed',
      errorType: 'Permission',
    },
    {
      id: 5,
      dateTime: '2026-04-05 14:32',
      pipeline: 'main/abc1235',
      status: 'process',
      errorType: 'Timeout',
    },
    {
      id: 6,
      dateTime: '2026-04-06 14:32',
      pipeline: 'main/abc1236',
      status: 'analyzed',
      errorType: 'Dependency',
    },
  ]

  const getStatusDisplay = (status) => {
    if (status === 'process') {
      return <span className="status process">⏳ В процессе</span>
    }
    return <span className="status analyzed">✅ Проанализировано</span>
  }

  const handleOpenAnalysis = (id) => {
    navigate(`/analysis/${id}`)
  }

  return (
    <div className="table-container">
      <table className="analysis-table">
        <thead>
          <tr>
            <th>Дата/Время</th>
            <th>Pipeline/Коммит</th>
            <th>Статус</th>
            <th>Тип ошибки</th>
            <th>Действие</th>
          </tr>
        </thead>
        <tbody>
          {analyses.map((item) => (
            <tr key={item.id}>
              <td>{item.dateTime}</td>
              <td>{item.pipeline}</td>
              <td>{getStatusDisplay(item.status)}</td>
              <td>{item.errorType}</td>
              <td>
                <button
                  className="btn-open"
                  onClick={() => handleOpenAnalysis(item.id)}
                >
                  Открыть
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button className="btn-show-more">Показать больше</button>
    </div>
  )
}

export default AnalysisTable