const baseURL = '/api'

const auth = '/auth'
const cars = '/cars'
const autoparks = '/auto_parks/1/cars'

const urls = {
    auth: {
        login: auth,
        socket: `${auth}/socket`
    },
    cars: cars,
    autoparks: autoparks
}

export {
    baseURL,
    urls
}