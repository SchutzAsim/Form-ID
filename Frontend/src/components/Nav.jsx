import React from 'react'
import { RiAddLargeLine } from "react-icons/ri";



export const Nav = () => {
    return (
        <>
            <nav>
                <div id='logo'>
                    Shop
                </div>
                <div className='add'>
                    <span>Add</span>
                    <RiAddLargeLine />
                </div>
            </nav>
        </>
    )
}
