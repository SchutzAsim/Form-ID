import { useState } from 'react'
import { Nav } from './components/Nav'
import { Home } from './components/Home'
import { LogForm } from './components/LogForm'
import { CardForm } from './components/CardForm'
import { ContainerContext } from './Context/context'


function App() {

  const API_Connect = import.meta.env.VITE_API;
  const [Show, setShow] = useState("home")
  const [isUpdate, setisUpdate] = useState(false)
  const [newForm, setnewForm] = useState(false)
  const [updateForm, setupdateForm] = useState(false)
  const [oldData, setoldData] = useState({})

  return (
    <>
      <ContainerContext.Provider
        value={
          {
            API_Connect,
            Show,
            setShow,
            isUpdate,
            setisUpdate,
            newForm,
            setnewForm,
            updateForm,
            setupdateForm,
            oldData,
            setoldData
          }
        }>

        <div className={`container`}>
          <Nav />
          <Home />
          <LogForm />
          <CardForm />
        </div>
      </ContainerContext.Provider>
    </>
  )
}

export default App
