import { useState } from 'react'
import { Login } from './components/Login'
import { Nav } from './components/Nav'
import { Home } from './components/Home'
import { LogForm } from './components/LogForm'
import { CardForm } from './components/CardForm'
import { ContainerContext } from './Context/context'
import { Routes, Route, useNavigate } from 'react-router-dom'


function App() {

  const API_Connect = import.meta.env.VITE_API;
  const access_token = localStorage.getItem('token')
  // const login_state = 'authorized'
  // let authorized = localStorage.getItem(login_state)

  const [oldData, setoldData] = useState({ id: "undefine" })

  const [searchPara, setsearchPara] = useState({
    query: ''
  })
  const [searchData, setsearchData] = useState([])

  const [authorized, setAuthorized] = useState(false)
  console.log(`login State: ${authorized}`)

  return (
    <>
      <ContainerContext.Provider
        value={
          {
            API_Connect,
            access_token,
            oldData,
            setoldData,
            searchPara,
            setsearchPara,
            searchData,
            setsearchData,
            authorized,
            setAuthorized
          }
        }>

        <Nav />
        <div className={`container`}>
          <Routes>
            <Route path='/login' element={<Login />} />
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
