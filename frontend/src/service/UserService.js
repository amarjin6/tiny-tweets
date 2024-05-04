import axios from "axios";

export default class UserService {
    getUserByUsername(config, currentUser) {
        let res = axios.get(`api/v1/users/${currentUser}`, config)
        return res
    }

    uploadUserProfileImage(file, username) {
        return axios.post(`/users/${username}/image/upload`, file, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        })
    }

    editProfile(body, config, id) {
        return axios.patch(`api/v1/users/${id}/`, body, config)
    }
}