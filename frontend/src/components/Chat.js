import {useEffect, useRef, useState} from "react";
import {socketService} from "../services/socketService";

const Chat = () => {
    const [room, setRoom] = useState(null)
    const [socketClient, setSocketClient] = useState(null)
    const [messages, setMessages] = useState([])

    const roomInput = useRef();

    useEffect(() => {
        if (room) {
            socketInit(room).then(client => setSocketClient(client))
        }
    }, [room]);

    const socketInit = async (room) => {
        const {chat} = await socketService();
        const client = await chat(room);

        client.onopen = () => {
            console.log('Chat socket connected');
        }

        client.onmessage = ({data}) => {
            const {body, user} = JSON.parse(data.toString());
            setMessages(prevState => [...prevState, {user, body}])
        }
        return client
    }
    const setRoomHandler = () => {
        console.log(roomInput.current.value);
        setRoom(roomInput.current.value)
    };


    const handlePressEnter = (e) => {
        if (e.key === 'Enter') {
            socketClient.send(JSON.stringify({
                data: e.target.value,
                action: 'send_message',
                request_id: new Date().getTime()
            }))
            e.target.value = ''
        }

    };

    return (
        <div>
            {!room &&
                <div>
                    <h2>Enter room</h2>
                    <input type="text" ref={roomInput}/>
                    <button onClick={setRoomHandler}>set</button>
                </div>
            }
            {
                room &&
                <div>
                    <h2>Enter message</h2>
                    {messages.map(message => <div>{message.user}: {message.body}</div>)}
                    <input type="text" onKeyDown={handlePressEnter}/>
                </div>

            }
        </div>
    );
};

export {Chat};