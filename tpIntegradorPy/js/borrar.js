const URL = "http://127.0.0.1:5000/"
// Obtiene el contenido del inventario
function obtenerProductos() {
fetch(URL + 'mueble') // Realiza una solicitud GET al servidor y obtener la lista de productos.
.then(response => {
// Si es exitosa (response.ok), convierte los datos de la respuesta de formato JSON a un objeto JavaScript.

if (response.ok) { return response.json(); }
})
// Asigna los datos de los productos obtenidos a lapropiedad productos del estado.
.then(data => {
const productosTable = document.getElementById('productos-table').getElementsByTagName('tbody')[0];

productosTable.innerHTML = ''; // Limpia la tabla antes de insertar nuevos datos

data.forEach(muebles => {
const row = productosTable.insertRow();
row.innerHTML = `
<td>${muebles.cod_articulo}</td>
<td>${muebles.nombre}</td>
<td>${muebles.descripcion}</td>
<td>${muebles.material}</td>
<td>${muebles.cantidad}</td>
<td >${muebles.preciomin}</td>
<td >${muebles.preciomay}</td>
<td><button onclick="eliminarProducto('${muebles.cod_articulo}')">Eliminar</button></td>
`;
});
})
// Captura y maneja errores, mostrando una alerta en caso de error al obtener los productos.
.catch(error => {
console.log('Error:', error);
alert('Error al obtener los productos.');
});
}
// Se utiliza para eliminar un producto.
function eliminarProducto(codigo) {
// Se muestra un diálogo de confirmación. Si el usuario confirma, 
//se realiza una solicitud DELETE al servidor a través de fetch(URL + 'productos/${codigo}', {method: 'DELETE' }).

if (confirm('¿Estás seguro de que quieres eliminar este producto?')) {

fetch(URL + 'mueble/' + {codigo} , { method: 'DELETE' })
.then(response => {
if (response.ok) {
    console.log(response);
// Si es exitosa (response.ok), elimina el producto y da mensaje de ok.

obtenerProductos(); // Vuelve a obtener la lista de productos para actualizar la tabla.

alert('Producto eliminado correctamente.');
}
})
// En caso de error, mostramos una alerta con un mensaje de error.

.catch(error => {
alert(error.message);
});
}
}
// Cuando la página se carga, llama a obtenerProductos para cargar la lista de productos.
document.addEventListener('DOMContentLoaded', obtenerProductos);