import React from 'react'
import { useState, useEffect } from 'react'

export const Home = () => {

    const DB_API = "http://localhost:8000"

    const [HomeData, setHomeData] = useState([])

    useEffect(() => {
        const api_connect = async () => {
            try {
                let res = await fetch(`${DB_API}/home`);
                if (!res.ok) console.log("Unable to connect HomeDataBase!");

                let HomeData = await res.json();
                setHomeData(HomeData);
            }
            catch (err) {
                console.error(`Error Occure in Backend Connection ${err}`)
            }
        }


        api_connect();


    }, [DB_API])

    // console.log(HomeData)


    return (
        <>
            <div className="card-container">
                {HomeData.map((row) => (
                    <div key={row.id} className="service-card">
                        {/* Card Header: Name and ID */}
                        <div className="card-header">
                            <h3 className="user-name">{row.Name}</h3>
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
                                <span className="label">Month</span>
                                <span className="value">{row.Month}</span>
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
                                    <span className="value">{row.Total_Amount}</span>
                                </div>
                                <div className="data-row due-row">
                                    <span className="label">Due Amount</span>
                                    <span className="value">{row.Due}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </>
    )
}