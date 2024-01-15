import {authService} from "./authService";
import {w3cwebsocket as W3cWebsocket} from 'websocket';

const baseURL = 'ws://localhost/api'

const socketService = async () => {
    const {data: {token}} = await authService.getSocketToken();
    return {
        chat: (room) => new W3cWebsocket(`${baseURL}/chat/${room}/?token=${token}`)
    }
}

export {
    socketService
}