/*para el menu hamburg*/
//const URL = "http://127.0.0.1:5000/";
const nav = document.querySelector("#nav");
const abrir = document.querySelector("#abrir");
const cerrar = document.querySelector("#cerrar");


/* para que se vea */
abrir.addEventListener("click", () => {
  nav.classList.add("visible");
});
/* para que se oculte */
cerrar.addEventListener("click", () => {
  nav.classList.remove("visible");
});

/***********carrusel de pagina muebles***********************/

'use strict'

const grande    = document.querySelector('.grande')
const punto     = document.querySelectorAll('.punto')

// Cuando CLICK en punto
    // Saber la posición de ese punto
    // Aplicar un transform translateX al grande
    // QUITAR la clase activo de TODOS puntos
    // AÑADIR la clase activo al punto que hemos hecho CLICK

// Recorrer TODOS los punto
punto.forEach( ( cadaPunto , i )=> {
    // Asignamos un CLICK a cadaPunto
    punto[i].addEventListener('click',()=>{

        // Guardar la posición de ese PUNTO
        let posicion  = i
        // Calculando el espacio que debe DESPLAZARSE el GRANDE
        let operacion = posicion * -50

        // MOVEMOS el grand
        grande.style.transform = `translateX(${ operacion }%)`

        // Recorremos TODOS los punto
        punto.forEach( ( cadaPunto , i )=>{
            // Quitamos la clase ACTIVO a TODOS los punto
            punto[i].classList.remove('activo')
        })
        // Añadir la clase activo en el punto que hemos hecho CLICK
        punto[i].classList.add('activo')

    })
})

/***********        pagina contacto      ***********************/
function validarFormulario() {
  let nombre = document.getElementById("nombre").value;
  let email = document.getElementById("email").value;
  let asunto = document.getElementById("asunto").value;
  let mensaje = document.getElementById("mensaje").value;
  let medioContacto = document.querySelector('input[name="medioContacto"]:checked');

  let errores = false;

  if (nombre === "") {
      document.getElementById("errorNombre").textContent = "El nombre es obligatorio";
      errores = true;
  } else {
      document.getElementById("errorNombre").textContent = "";
  }

  if (email === "") {
      document.getElementById("errorEmail").textContent = "El correo electrónico es obligatorio";
      errores = true;
  } else {
      if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
          document.getElementById("errorEmail").textContent = "El correo electrónico no es válido";
          errores = true;
      } else {
          document.getElementById("errorEmail").textContent = "";
      }
  }

  if (asunto === "") {
      document.getElementById("errorAsunto").textContent = "El asunto es obligatorio";
      errores = true;
  } else {
      document.getElementById("errorAsunto").textContent = "";
  }

  if (mensaje === "") {
      document.getElementById("errorMensaje").textContent = "El mensaje es obligatorio";
      errores = true;
  } else {
      document.getElementById("errorMensaje").textContent = "";
  }

  if (!medioContacto) {
      document.getElementById("errorMedioContacto").textContent = "Debe seleccionar un medio de contacto";
      errores = true;
  } else {
      document.getElementById("errorMedioContacto").textContent = "";
  }

  return !errores;
}









