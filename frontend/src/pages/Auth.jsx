import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function Auth() {
  const [isLogin, setIsLogin] = useState(true)
  const navigate = useNavigate()

  const handleLogin = (e) => {
    e.preventDefault()
    navigate('/catalog')
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h1 className="auth-logo">ci-ai</h1>

        <div className="auth-tabs">
          <button
            className={isLogin ? 'active' : ''}
            onClick={() => setIsLogin(true)}
          >
            Вход
          </button>
          <button
            className={!isLogin ? 'active' : ''}
            onClick={() => setIsLogin(false)}
          >
            Регистрация
          </button>
        </div>

        <form onSubmit={handleLogin} className="auth-form">
          <div className="form-group">
            <label>Email</label>
            <input type="email" placeholder="email@example.com" defaultValue="email@example.com" />
          </div>

          <div className="form-group">
            <label>Пароль</label>
            <input type="password" placeholder="••••••••" defaultValue="password" />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label>Повторите пароль</label>
              <input type="password" placeholder="••••••••" />
            </div>
          )}

          <button type="submit" className="btn-primary">
            {isLogin ? 'Войти' : 'Зарегистрироваться'}
          </button>

          {isLogin && <a href="#" className="forgot-link">Забыли пароль?</a>}
        </form>
      </div>
    </div>
  )
}

export default Auth