import React, { useContext } from 'react'
import { useState, useEffect } from 'react';
import { RiAddLargeLine } from "react-icons/ri";
import { useNavigate } from 'react-router-dom';
import { ContainerContext } from '../Context/context';



export const Nav = () => {
    const { API_Connect, searchPara, setsearchPara, setsearchData } = useContext(ContainerContext)

    const navigate = useNavigate();


    const handleChange = (e) => {
        const { name, value } = e.target;
        setsearchPara({
            ...searchPara,
            [name]: value
        })
    }


    const handleRoute = () => {
        navigate("/new/post")
    }

    let searchPathWords = searchPara.query.split(' ')
    let searchPath = searchPathWords.join('+')
    const handleSearchPage = () => {
        navigate(`/post/search/${searchPath}`)
    }


    const handleSearch = async (data) => {
        data.preventDefault()

        // API call here
        try {
            const res = await fetch(`${API_Connect}/search/post/${searchPara.query}`, {
                method: "GET",
                headers: {
                    "content-type": "application/json"
                }
            })

            if (!res.ok) throw Error("search request failed!")

            let post_res = await res.json()
            setsearchData(post_res)
            return post_res
        }
        catch (err) {
            console.error(`Error Occure in Posting Form with error code ${err}`)
        }
        finally {
            handleSearchPage()
        }
    }


    return (
        <>
            <nav>
                <div id='logo' onClick={() => navigate("/")}>
                    Shop
                </div>
                <form className="search-bar form-group" onSubmit={handleSearch}>
                    <input type="text" className="search-area" name='query' placeholder='Search' value={searchPara.query} onChange={handleChange} />
                </form>
                <div className="btnholder">
                    <div onClick={() => (handleRoute())} className='add'>
                        <RiAddLargeLine />
                    </div>
                </div>
            </nav>
        </>
    )
}
