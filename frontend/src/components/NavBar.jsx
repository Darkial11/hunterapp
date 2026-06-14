import { NavLink } from 'react-router-dom'
import './NavBar.css'

const navItems = [
  { to: '/home', icon: '⚔️', label: 'Inicio' },
  { to: '/missions', icon: '📋', label: 'Misiones' },
  { to: '/rewards', icon: '🎁', label: 'Recompensas' },
  { to: '/achievements', icon: '🏆', label: 'Logros' },
  { to: '/config', icon: '⚙️', label: 'Config' },
]

export default function NavBar() {
  return (
    <nav className="navbar">
      {navItems.map(item => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <span className="nav-icon">{item.icon}</span>
          <span className="nav-label">{item.label}</span>
        </NavLink>
      ))}
    </nav>
  )
}