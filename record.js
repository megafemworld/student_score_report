document.getElementById('loginform').addEventListener('submit', function(event) {
    var username = document.getElementById('user_id').value;

    if (!/^[A-Z]{2}/.test(username)) {
        event.preventDefault();  
        alert('Username must start with two capital letters!');
    }
});