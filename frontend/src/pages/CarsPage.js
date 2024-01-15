import {Chat} from "../components/Chat";
import {CarForm} from "../components/CarForm";
import {Cars} from "../components/Cars";

const CarsPage = () => {
    return (
        <div>
            <CarForm/>
            <Cars/>
            <Chat/>
        </div>
    );
};

export {CarsPage};