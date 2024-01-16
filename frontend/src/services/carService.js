import {axiosService} from "./axiosService";
import {urls} from "../constants/urls";

const carService = {
    getAll:()=>axiosService.get(urls.cars),
    create:(data)=> axiosService.post(urls.autoparks,data)
}

export {
    carService
}