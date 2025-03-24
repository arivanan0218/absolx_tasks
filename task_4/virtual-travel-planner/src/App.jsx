import Navbar from './components/layout/Navbar'
import Home from './pages/Home'
import './App.css'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main>
        <Home />
      </main>
    </div>
  )
}

export default App
