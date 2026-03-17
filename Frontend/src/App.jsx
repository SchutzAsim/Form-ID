import { useState } from 'react'
import { Nav } from './components/Nav'
import { Home } from './components/Home'
import { LogForm } from './components/LogForm'
import { ContainerContext } from './Context/context'


function App() {

  const API_Connect = import.meta.env.VITE_API;
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
