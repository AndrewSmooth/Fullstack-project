import { Link, useLocation } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'

function Header() {
  const location = useLocation()
  const navigate = useNavigate();

  const navItems = [
    { path: '/catalog', label: 'Анализы' },
    { path: '/upload', label: 'Новый анализ' },
    { path: '/analytics', label: 'Аналитика' }
  ]

  return (
    <header className="header">
      <div className="header-top">
        <h1 className="logo">ci-ai</h1>
        <nav className="nav">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="header-right">
          <div className="user-avatar">○</div>
          <button className="logout-btn" onClick={() => navigate('/')}>Выйти</button>
        </div>
      </div>
    </header>
  )
}

export default Header