function switchToRegister() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
    document.getElementById('success-message').style.display = 'none';
    document.getElementById('error-message').style.display = 'none';
}

function switchToLogin() {
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('success-message').style.display = 'none';
    document.getElementById('error-message').style.display = 'none';
}

function handleRegister(event) {
    event.preventDefault();
    const form = document.getElementById('register-form-element');
    const formData = new FormData(form);

    fetch('/signup', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('register-form').style.display = 'none';
            document.getElementById('success-message').style.display = 'block';
        } else {
            document.getElementById('register-form').style.display = 'none';
            document.getElementById('error-message').style.display = 'block';
            document.getElementById('error-text').innerText = data.message;
        }
    })
    .catch(error => {
        document.getElementById('register-form').style.display = 'none';
        document.getElementById('error-message').style.display = 'block';
        document.getElementById('error-text').innerText = '註冊過程中發生錯誤，請稍後再試。';
    });
}
