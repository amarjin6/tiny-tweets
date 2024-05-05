import React, {useState} from 'react';
import SearchIcon from '@mui/icons-material/Search';
import PeopleIcon from '@mui/icons-material/People';
import ChatIcon from '@mui/icons-material/Chat';
import bg from '../images/friends_meal.jpg'
import {ReactComponent as Myicon} from '../images/twitter.svg'
import AuthService from "../service/AuthService";
import {useDispatch} from "react-redux";
import {login} from "../redux/reduxSlice";
import {useNavigate} from "react-router-dom";

const Home = () => {
    const [username, setUsername] = useState(null)
    const [password, setPassword] = useState(null)

    const dispatch = useDispatch()
    const navigate = useNavigate()
    const loginClick = (e) => {
        let body = {
            email: username,
            password: password
        }
        let authService = new AuthService()
        authService.login(body).then(res => {
            dispatch(login(res.data))
        })
        e.preventDefault()
    }

    return (
        <div className="flex flex-col w-full h-screen m-0" style={{fontFamily: `Segoe UI, Arial, sans-serif`}}>
            <div className="flex flex-row h-screen">
                <div className="flex w-1/2"
                     style={{
                         backgroundImage: `url(${bg}`,
                         backgroundColor: "rgba(87, 89, 93, 0.8)",
                         backgroundRepeat: "no-repeat",
                         backgroundSize: "cover"
                     }}>
                    <div className="flex flex-col justify-center w-full text-white">
                        <div className="flex flex-row items-center max-w-md w-full ml-auto mr-auto mb-12 font-bold text-xl border-blue-600 border-2 p-2 rounded-lg shadow-lg" style={{ backdropFilter: "blur(3px)", boxShadow: "0 10px 20px rgba(0, 0, 0, 0.5)" }}>
                            <SearchIcon fontSize="large" style={{ marginRight: "5px" }} className="rounded-full shadow-lg"/>
                            <span className="font-bold text-xl">Follow your interests</span>
                        </div>
                        <div className="flex flex-row items-center max-w-md w-full ml-auto mr-auto mb-12 font-bold text-xl border-green-600 border-2 p-2 rounded-lg shadow-lg" style={{ backdropFilter: "blur(3px)", boxShadow: "0 10px 20px rgba(0, 0, 0, 0.5)" }}>
                        <PeopleIcon fontSize="large" style={{ marginRight: "5px" }} className="rounded-full shadow-lg"/>
                        <span className="font-bold text-xl">Hear what your people are talking about</span>
                    </div>
                        <div className="flex flex-row items-center max-w-md w-full ml-auto mr-auto mb-12 font-bold text-xl border-red-500 border-2 p-2 rounded-lg shadow-lg" style={{ backdropFilter: "blur(3px)", boxShadow: "0 10px 20px rgba(0, 0, 0, 0.5)" }}>
                            <ChatIcon fontSize="large" style={{ marginRight: "5px" }} className="rounded-full shadow-lg"/>
                            <span className="font-bold text-xl">Join the conversation</span>
                        </div>
                    </div>
                </div>
                <div className="flex flex-col space-x-reverse w-1/2">
                    <form className="flex justify-center w-full mt-5">
                        <div className="mr-2.5">
                            <input type="text"
                                   placeholder="Email"
                                   className="border-b p-3 block placeholder-gray-dark bg-transparent focus:outline-none w-full text-sm focus-within:ring-1 focus-within:ring-primary-base"
                                   onChange={e => setUsername(e.target.value)}/>
                        </div>
                        <div className="mr-2.5">
                            <input type="password"
                                   placeholder="Password"
                                   className="border-b p-3 block placeholder-gray-dark bg-transparent focus:outline-none w-full text-sm focus-within:ring-1 focus-within:ring-primary-base"
                                   onChange={e => setPassword(e.target.value)}/>
                            <a className="text-gray-400 text-xs ml-3">Don't have an account? Sign up</a>
                        </div>
                        <button
                            className="bg-transparent py-2 px-4 rounded-2xl p-3 text-blue-400 text-sm box-border w-auto h-11 font-bold"
                            style={{color: "#1DA1F2", border: `1px solid #57595d`}} type="submit"
                            onClick={loginClick}>Log in
                        </button>
                    </form>
                    <div className="max-h-72 m-auto max-w-sm">
                        <Myicon fill="blue" style={{marginLeft: "-30px" }}/>
                        <h1 className="text-2xl mb-3 font-bold" style={{lineHeight: "32px", color: "#1DA1F2"}}>See what's happening in
                            <br/> the world right now</h1>
                        <span style={{color: "#57595d"}}>Join Tiny Tweets today.</span>
                        <button
                            className="flex justify-center items-center w-full h-11 text-white font-bold py-2 px-4 rounded-2xl mt-3"
                            style={{backgroundColor: "#1DA1F2", border: `1px solid #eeeeef`}}
                            onClick={() => navigate("/signup")}>Sign up
                        </button>
                        <button
                            className="flex justify-center items-center w-full h-11 bg-transparent py-2 px-4 rounded-2xl mt-1"
                            style={{color: "#57595d", border: `1px solid #57595d`}}
                            onClick={() => navigate("/login")}> Log in
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;