import { Nav } from './components/Nav'
import { Home } from './components/Home'
import { LogForm } from './components/LogForm'
import { useState } from 'react'
import { ContainerContext } from './Context/context'


function App() {

  const API_Connect = "http://0.0.0.0:8000"
  const [Show, setShow] = useState("home")

  return (
    <>
      <ContainerContext.Provider
        value={
          {
            Show,
            setShow,
            API_Connect
          }
        }>

        <div className="container">
          <Nav />
          <Home />
          <LogForm />
        </div>
      </ContainerContext.Provider>
    </>
  )
}

export default App
