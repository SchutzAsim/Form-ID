import { useState, useEffect } from 'react'
import { Nav } from './components/Nav'
import { Home } from './components/Home'
import { LogForm } from './components/LogForm'
import { CardForm } from './components/CardForm'
import { ContainerContext } from './Context/context'
import { Routes, Route } from 'react-router-dom'


function App() {

  const API_Connect = import.meta.env.VITE_API;

  const [oldData, setoldData] = useState({ id: "undefine" })

  const [searchPara, setsearchPara] = useState({
    query: ''
  })
  const [searchData, setsearchData] = useState([])

  return (
    <>
      <ContainerContext.Provider
        value={
          {
            API_Connect,
            oldData,
            setoldData,
            searchPara,
            setsearchPara,
            searchData,
            setsearchData
          }
        }>

        <Nav />
        <div className={`container`}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/post/search/:query" element={<Home />} />
            <Route path="/new/post" element={<LogForm />} />
            <Route path={`/update/log`} element={<CardForm />} />
          </Routes>
        </div>
      </ContainerContext.Provider>
    </>
  )
}

export default App
