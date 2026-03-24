import React from 'react'
import { useState } from 'react';
import { useContext } from 'react';
import { ContainerContext } from '../Context/context';

export const LogForm = () => {


    const { API_Connect, Show, setShow } = useContext(ContainerContext);


    const [formData, setFormData] = useState({
        Name: '',
        Contact: '',
        Service: '',
        Service_Type: '',
        Govt_Fee: 0,
        Service_Charge: 0,
        Total_Amount: 0,
        Month: '',
        Created_At: 'Default',
        Application_ID: 'NA',
        Due: 0
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (data) => {
        data.preventDefault();
        
        // API call here
        try {
            const res = await fetch(`${API_Connect}/post`, {
                method: "POST",
                headers: {
                    "content-type": "application/json"
                },
                
                body: JSON.stringify(formData)
                
            })
            if (!res.ok) throw Error("post request failed!")
                
                let post_res = await res.json()
                return post_res
            }
            catch (err) {
                console.error(`Error Occure in Posting Form with error code ${err}`)
            }
            
        };
        
    if (Show === "form") {
        return (<>
            <div className={`form-page-container`}>
                <form className="theme-form" onSubmit={handleSubmit}>
                    <div className="form-header">
                        <h2>Add New Log</h2>
                        <p>Enter the service details below.</p>
                    </div>

                    <div className="form-grid">
                        {/* Text Inputs */}
                        <div className="form-group">
                            <label>Name</label>
                            <input type="text" name="Name" value={formData.Name} onChange={handleChange} placeholder='Name' required />
                        </div>

                        <div className="form-group">
                            <label>Contact</label>
                            <input type="text" name="Contact" value={formData.Contact} onChange={handleChange} placeholder='1234567890' required />
                        </div>

                        <div className="form-group">
                            <label>Service</label>
                            <input type="text" name="Service" value={formData.Service} onChange={handleChange} placeholder='Service' required />
                        </div>

                        <div className="form-group">
                            <label>Service Type</label>
                            <input type="text" name="Service_Type" value={formData.Service_Type} onChange={handleChange} placeholder='Service Type' required />
                        </div>

                        <div className="form-group">
                            <label>Month</label>
                            {/* Could also be type="month" depending on your needs */}
                            <input type="text" name="Month" value={formData.Month} onChange={handleChange} placeholder="e.g. Jan26" required/>
                        </div>

                        <div className="form-group">
                            <label>Created At</label>
                            <input type="text" name="Created_At" value={formData.Created_At} onChange={handleChange} placeholder='e.g. YYYY-MM-DD' required/>
                        </div>

                        <div className="form-group full-width">
                            <label>Application ID</label>
                            <input type="text" name="Application_ID" value={formData.Application_ID} onChange={handleChange} placeholder='Application no.'/>
                        </div>

                        {/* Financial/Integer Inputs */}
                        <div className="form-group">
                            <label>Govt Fee</label>
                            <input type="number" name="Govt_Fee" value={formData.Govt_Fee} onChange={handleChange} />
                        </div>

                        <div className="form-group">
                            <label>Service Charge</label>
                            <input type="number" name="Service_Charge" value={formData.Service_Charge} onChange={handleChange} />
                        </div>

                        <div className="form-group">
                            <label>Total Amount</label>
                            <input type="number" name="Total_Amount" value={formData.Total_Amount} onChange={handleChange} />
                        </div>

                        <div className="form-group">
                            <label>Due</label>
                            <input type="number" name="Due" value={formData.Due} onChange={handleChange} />
                        </div>
                    </div>

                    {/* <div className=""> */}
                    <div className="form-actions btn">
                        <button type="submit" className="submit-btn btn">Save Log</button>
                    </div>
                    <div className="form-actions btn">
                        <button onClick={() => setShow("home")} type="submit" className="submit-btn btn">Cancel</button>
                    </div>
                    {/* </div> */}
                </form>
            </div>
        </>)
    }
}
