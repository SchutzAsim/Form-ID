import React from 'react'
import { RiAddLargeLine } from "react-icons/ri";
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { ContainerContext } from '../Context/context';



export const Nav = () => {

    const { setShow, setupdateForm, setnewForm } = useContext(ContainerContext)

    const navigate = useNavigate();

    const handleRoute = () => {
        navigate("/new/post")
    }


    return (
        <>
            <nav>
                <div id='logo' onClick={() => navigate("/")}>
                    Shop
                </div>
                <div className="btnholder">
                    <div onClick={() => (setShow("form"), setnewForm(true), setupdateForm(false), handleRoute())} className='add'>
                        <RiAddLargeLine />
                    </div>
                </div>
            </nav>
        </>
    )
}
