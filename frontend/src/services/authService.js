import {axiosService} from "./axiosService";
import {urls} from "../constants/urls";

const authService = {
    async login(user) {
        const {data: {access}} = await axiosService.post(urls.auth.login, user);
        localStorage.setItem('access_token', access)
    },
    getSocketToken() {
        return axiosService.get(urls.auth.socket)
    }
}

export {
    authService
}