//const URL = "http://127.0.0.1:5000/"
// Al subir al servidor, deberá utilizarse la siguiente ruta.
//USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
const URL = "https://mansama18.pythonanywhere.com/"
// Variables de estado para controlar la visibilidad y los datos del formulario

let codigo = '';
let nombre = '';
let descripcion = '';
let material = '';
let cantidad = '';
let preciomn = '';
let preciomy = '';
//let imagen_url = '';
//let imagenSeleccionada = null;
//let imagenUrlTemp = null;
let mostrarDatosProducto = false;

document.getElementById('form-obtener-producto').addEventListener('submit', obtenerProducto);

