import React from 'react'
import { ImCancelCircle } from "react-icons/im";
import { RiAddLargeLine } from "react-icons/ri";
import { MdModeEdit } from "react-icons/md";
import { useContext, useState, useEffect } from 'react';
import { ContainerContext } from '../Context/context';



export const Nav = () => {

    const { setShow, setupdateForm, setnewForm } = useContext(ContainerContext)

    return (
        <>
            <nav>
                <div id='logo'>
                    Shop
                </div>
                <div className="btnholder">
                    <div onClick={() => (setShow("form"), setnewForm(true), setupdateForm(false))} className='add'>
                        <RiAddLargeLine />
                    </div>
                    {/* <div onClick={() => (setupdateForm(true), setShow("updateform"))} className='add'>
                        <MdModeEdit />
                    </div> */}
                </div>
            </nav>
            {/* <div className="getid" style={isUpdate ? { display: 'flex' } : { display: 'none' }}>
                <div className='form-theme confirmation-Box'>
                    <div className="form-group">
                        <label className='cancel'>
                            <h3>Enter ID for Update</h3>
                            <ImCancelCircle size={25} color='#ff0606' onClick={() => setisUpdate(false)} />
                        </label>
                        <input type="text" name="id" placeholder='e.g. 1' required />
                    </div>
                    <div className="form-actions btn" style={{ marginTop: '4px' }} onClick={() => (setupdateForm(true), setShow(""))}>
                        <button type="submit" className="submit-btn btn">Update ID</button>
                    </div>
                </div>
            </div> */}
        </>
    )
}
