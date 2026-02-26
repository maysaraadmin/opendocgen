import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import DocumentGenerator from './pages/DocumentGenerator'
import TaskManager from './pages/TaskManager'
import FileManager from './pages/FileManager'

function App() {
  return (
    <Router>
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
        <h1>🚀 OpenDocGen - AI Document Generation</h1>
        <p>Welcome to the OpenDocGen frontend!</p>
        <div style={{ marginTop: '20px' }}>
          <h2>Available Pages:</h2>
          <ul>
            <li><a href="/">Dashboard</a></li>
            <li><a href="/generator">Document Generator</a></li>
            <li><a href="/tasks">Task Manager</a></li>
            <li><a href="/files">File Manager</a></li>
          </ul>
        </div>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/generator" element={<DocumentGenerator />} />
          <Route path="/tasks" element={<TaskManager />} />
          <Route path="/files" element={<FileManager />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
