import React from 'react'
import { RiAddLargeLine } from "react-icons/ri";
import { useNavigate } from 'react-router-dom';



export const Nav = () => {
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
                    <div onClick={() => (handleRoute())} className='add'>
                        <RiAddLargeLine />
                    </div>
                </div>
            </nav>
        </>
    )
}
