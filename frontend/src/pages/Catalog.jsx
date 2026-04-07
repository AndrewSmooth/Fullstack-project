import SearchFilters from '../components/SearchFilters'
import AnalysisTable from '../components/AnalysisTable'

function Catalog() {
  return (
    <div className="catalog-page">
      <h2 className="page-title">Экран 2: Каталог анализов</h2>
      <SearchFilters />
      <AnalysisTable />
    </div>
  )
}

export default Catalog