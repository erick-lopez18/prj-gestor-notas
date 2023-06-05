  // Obtener el token de autenticación desde alguna fuente (por ejemplo, almacenado en una cookie o en el almacenamiento local)
const token = 'django-insecure-6=m@4e^j$!@21r$qiy$db+tn#uj7it&6^7o#x72q+i!4^iu34&'; // Obtén el token de autenticación de donde lo almacenes

// Configurar los encabezados de la solicitud con el token de autenticación
const headers = {
  Authorization: `Bearer ${token}`,
  'Content-Type': 'application/json',
  'X-CSRFToken': getCookie('csrftoken'), // Reemplaza getCookie con la función adecuada para obtener el valor del token CSRF
};

// Realizar la solicitud AJAX utilizando Axios y los encabezados configurados
axios.post('/api/login/', {
  username: 'usuario',
  password: 'contraseña',
}, { headers })
  .then(response => {
    // Manejar la respuesta exitosa
    console.log(response.data);
  })
  .catch(error => {
    // Manejar el error
    console.error(error);
  });

  const loginForm = document.getElementById('login-form');

  loginForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Evitar el envío tradicional del formulario

    const formData = new FormData(loginForm);
    const url = loginForm.getAttribute('action');
    const method = loginForm.getAttribute('method');

    axios({
      method: method,
      url: url,
      data: formData,
    })
      .then(function (response) {
        // Manejar la respuesta exitosa
        console.log(response.data);
        // Redireccionar a la página deseada si es necesario
      })
      .catch(function (error) {
        // Manejar el error
        console.error(error);
        // Mostrar el mensaje de error en el template usando JavaScript
        const errorMessage = error.response.data.error;
        const errorContainer = document.getElementById('error-container');
        errorContainer.textContent = errorMessage;
      });
  });

  axios.post('/api/login/', data)
  .then(response => {
    const data = response.data;
    if (data.redirect === 'home') {
      window.location.href = '/home';
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });

// bootstrap no se
  const express = require("express")
  const path = require("path")
  
  const app = express()
  
  app.use(
    "/css",
    express.static(path.join(_dirname, "node_modules/bootstrap/dist/css"))
  )
  app.use(
    "/js",
    express.static(path.join(_dirname, "node_modules/bootstrap/dist/js"))
  )
  app.use("/js", express.static(path.join(_dirname, "node_modules/jquery/dist")))