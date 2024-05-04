import {createSlice} from "@reduxjs/toolkit";
import { jwtDecode } from 'jwt-decode';

export const reduxSlice = createSlice({
    name: 'redux',
    initialState: {
        currentUser: localStorage.getItem('currentUser'),
        username: localStorage.getItem('username'),
        accessToken: localStorage.getItem('accessToken'),
        profileImageLink: localStorage.getItem('image')
    },
    reducers: {
        login: (state, action) => {
            const user = jwtDecode(action.payload.access);
            localStorage.setItem('currentUser', user.user_id)
            localStorage.setItem('username', action.payload.username)
            localStorage.setItem('accessToken', action.payload.access)
            state.currentUser = user.user_id
            state.username = action.payload.username
            state.accessToken = action.payload.access
        },
        logout: state => {
            localStorage.removeItem('currentUser')
            localStorage.removeItem("username")
            localStorage.removeItem('accessToken')
            localStorage.removeItem('profileImageLink')
            state.currentUser = undefined
            state.username = undefined
            state.accessToken = undefined
            state.profileImageLink = undefined
        },
        setUserDetails: (state, action) => {
            localStorage.setItem('profileImageLink', action.payload.image)
            state.profileImageLink = action.payload.image
        },
    }
})
export const {login, logout, setUserDetails} = reduxSlice.actions
export default reduxSlice.reducer