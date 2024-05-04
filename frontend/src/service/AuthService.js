import axios from "axios";

export default class AuthService {

    login(body) {
        return axios.post("/api/v1/login/", body)
    }

    signup(body) {
        return axios.post("/api/v1/register/", body)
    }
}