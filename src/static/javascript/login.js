/*
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('.login-container form');
    
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar el envío del formulario por defecto
        
        const formData = new FormData(form);
        const formDataJson = {};
        
        formData.forEach((value, key) => {
            formDataJson[key] = value;
        });
        
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formDataJson)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Si la autenticación fue exitosa, redirige o muestra un mensaje de éxito
                console.log('Autenticación exitosa');
                console.log('Token:', data.token);
                // Aquí podrías redirigir a otra página o ejecutar alguna acción adicional
            } else {
                // Si la autenticación falla, muestra un mensaje de error
                console.error('Autenticación fallida');
                alert('Usuario o contraseña incorrectos');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error durante la autenticación');
        });
    });
});*/