import {useForm} from "react-hook-form";
import {carService} from "../services/carService";

const CarForm = () => {
    const token = localStorage.getItem("token");
    const config = {
        headers: {Authorization: `Bearer ${token}`}
    };
    const {register, handleSubmit} = useForm();

    const save = async (car) => {
        console.log(config)
        await carService.create(car, config)
    }
    return (
        <div>
            <h2>Create new car</h2>
            <form onSubmit={handleSubmit(save)}>
                <input type="text" placeholder={'brand'} {...register('brand')}/>
                <input type="text" placeholder={'price'} {...register('price')}/>
                <input type="text" placeholder={'year'} {...register('year')}/>
                <input type="text" placeholder={'body'} {...register('body')}/>
                <input type="text" placeholder={'number_of_seats'} {...register('number_of_seats')}/>
                <input type="text" placeholder={'engine_capacity'} {...register('engine_capacity')}/>
                <input type="text" placeholder={'currency'} {...register('currency')}/>
                <input type="text" placeholder={'region'} {...register('region')}/>
                <button>save</button>
            </form>
        </div>
    );
};

export {CarForm};