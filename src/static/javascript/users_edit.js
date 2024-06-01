document.addEventListener('DOMContentLoaded', function() {
    loadUserList();
    
    document.getElementById('userForm').addEventListener('submit', function(event) {
        event.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        fetch('/users_edit/annadir_usuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username, password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                alert('Usuario agregado correctamente');
                loadUserList(); // Recargar la lista de usuarios
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

function loadUserList() {
    fetch('/users_edit/get_users')
    .then(response => response.json())
    .then(data => {
        const userList = document.getElementById('userList');
        userList.innerHTML = '';
        data.users.forEach(user => {
            const listItem = document.createElement('li');
            listItem.textContent = user;

            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Eliminar';
            deleteButton.onclick = () => deleteUser(user);
            listItem.appendChild(deleteButton);

            userList.appendChild(listItem);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function deleteUser(username) {
    fetch('/users_edit/eliminar_usuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            alert('Usuario eliminado correctamente');
            loadUserList(); // Recargar la lista de usuarios
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}