import React from 'react'
import { useEffect, useContext, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom';
import { ContainerContext } from '../Context/context'
import { MdModeEdit } from "react-icons/md";


export const Home = () => {

    const { API_Connect, setoldData, searchData } = useContext(ContainerContext)

    const url = useLocation();

    const [HomeData, setHomeData] = useState([])
    let showonPage = url.pathname.startsWith("/post/search/") ? searchData : HomeData



    HomeData.reverse()

    useEffect(() => {
        const api_connect = async () => {
            try {
                let res = await fetch(`${API_Connect}/home`);
                if (!res.ok) console.log("Unable to connect HomeDataBase!");

                let HomeData = await res.json();
                setHomeData(HomeData);
            }
            catch (err) {
                console.error(`Error Occure in Backend Connection ${err}`)
            }
        }

        api_connect();


    }, [API_Connect, url.pathname])

    const navigate = useNavigate();
    const handleRoute = () => {
        navigate(`/update/log`)
    }

    return (
        <>
            <div className={`card-container`}>
                { showonPage.map((row) => (
                    <div key={row.id} className="service-card">
                        {/* Card Header: Name and ID */}
                        <div className="card-header">
                            <div className="editBox">
                                <h3 className="user-name">{row.Name}</h3>
                                <div onClick={() => (setoldData(row), handleRoute())}>
                                    <MdModeEdit size='25' />
                                </div>
                            </div>
                            <span className="user-id">ID: {row.id}</span>
                        </div>

                        {/* Card Body: All other details */}
                        <div className="card-body">
                            <div className="data-row">
                                <span className="label">Contact</span>
                                <span className="value">{row.Contact}</span>
                            </div>
                            <div className="data-row">
                                <span className="label">Service</span>
                                <span className="value">{row.Service}</span>
                            </div>
                            <div className="data-row">
                                <span className="label">Service Type</span>
                                <span className="value">{row.Service_Type}</span>
                            </div>
                            <div className="data-row">
                                <span className="label">Created At</span>
                                <span className="value">{row.Created_At}</span>
                            </div>
                            <div className="data-row">
                                <span className="label">Application ID</span>
                                <span className="value">{row.Application_ID}</span>
                            </div>

                            {/* Financials grouped together visually */}
                            <div className="financials">
                                <div className="data-row">
                                    <span className="label">Govt Fee</span>
                                    <span className="value">₹{row.Govt_Fee}</span>
                                </div>
                                <div className="data-row">
                                    <span className="label">Service Fee</span>
                                    <span className="value">₹{row.Service_Charge}</span>
                                </div>
                                <div className="data-row total-row">
                                    <span className="label">Total Fee</span>
                                    <span className="value">₹{row.Total_Amount}</span>
                                </div>
                                <div className="data-row due-row">
                                    <span className="label">Due Amount</span>
                                    <span className="value">₹{row.Due}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </>
    )
}

