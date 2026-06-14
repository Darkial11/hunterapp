import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import NavBar from './components/NavBar'
import Home from './pages/Home'
import Missions from './pages/Missions'
import Stats from './pages/Stats'
import Achievements from './pages/Achievements'
import Rewards from './pages/Rewards'
import Config from './pages/Config'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <div className="page-content">
          <Routes>
            <Route path="/" element={<Navigate to="/home" />} />
            <Route path="/home" element={<Home />} />
            <Route path="/missions" element={<Missions />} />
            <Route path="/stats" element={<Stats />} />
            <Route path="/achievements" element={<Achievements />} />
            <Route path="/rewards" element={<Rewards />} />
            <Route path="/config" element={<Config />} />
          </Routes>
        </div>
        <NavBar />
      </div>
    </BrowserRouter>
  )
}

export default App