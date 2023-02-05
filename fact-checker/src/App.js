import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Analyser from './components/Pages/Analyser';
import Navbar from './components/Navbar'
import './App.css'

function App() {
  return (
    <div>
        <Navbar />
        <Router>
            <Routes>
                <Route path="/" element={<Analyser />} />
            </Routes>
        </Router>
    </div>
  );
}
export default App