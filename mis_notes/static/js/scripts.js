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