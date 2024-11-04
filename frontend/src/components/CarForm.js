import {useForm} from "react-hook-form";
import {carService} from "../services/carService";

const CarForm = () => {
    const {register, handleSubmit} = useForm();

    const save = async (car) => {
        await carService.create(car)
    }
    return (
        <form onSubmit={handleSubmit(save)}>
            <input type="text" placeholder={'brand'} {...register('brand')}/>
            <input type="text" placeholder={'price'} {...register('price')}/>
            <input type="text" placeholder={'year'} {...register('year')}/>
            <input type="text" placeholder={'body'} {...register('body')}/>
            <button>save</button>
        </form>
    );
};

export {CarForm};