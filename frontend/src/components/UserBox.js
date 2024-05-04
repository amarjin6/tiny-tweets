import React, {useEffect, useState} from "react";
import LogoutIcon from '@mui/icons-material/Logout';
import {useDispatch, useSelector} from "react-redux";
import {logout, setUserDetails} from "../redux/reduxSlice";
import UserService from "../service/UserService";
import {useNavigate} from "react-router-dom";
import profile from "../images/default-profile.png"

const UserBox = () => {
    const currentUser = useSelector(state => state.reduxSlice.currentUser)
    const accessToken = useSelector(state => state.reduxSlice.accessToken)

     let config = {
        headers: {
            'Authorization': 'Bearer ' + accessToken
        }
     }

    const [user, setUser] = useState()

    useEffect(() => {
        let userService = new UserService()
        userService.getUserByUsername(config, currentUser).then(res => {
            setUser(res.data)
            dispatch(setUserDetails(res.data))
        })
    }, [currentUser])

    const navigate = useNavigate()

    const dispatch = useDispatch()

    const logoutClick = () => {
        dispatch(logout())
    }
    return (
        <>
            {user &&
                <div
                    className="flex items-center mb-6 hover:bg-primary-light cursor-pointer rounded-full py-2 px-4 transform transition-colors duration-200"
                    onClick={() => navigate("/")}>
                    <img
                        src={user.image}
                        alt="Profile"
                        className="w-11 h-11 rounded-full"
                    />
                    <div className="flex flex-col ml-3">
                        <span className="font-bold text-md text-black">{user.first_name}</span>
                        <span className="text-sm text-gray-dark">@{user.username}</span>
                    </div>
                    <LogoutIcon style={{marginLeft: "auto"}} onClick={logoutClick}/>
                </div>}
        </>
    );
};

export default UserBox;
