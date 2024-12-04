import axios, {request} from "axios";
import {baseURL} from "../constants/urls";

const axiosService = axios.create({baseURL})

axiosService.interceptors.request.use(request => {
    const token = localStorage.getItem('access_token');

    if (token) {
        request.headers.Authorization = `Bearer ${token}`
    }

    return request
})

export {
    axiosService
}