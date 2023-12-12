
<template>
            <div class="col-lg-9 p-3 d-flex justify-content-center align-items-center" style="background-color: #e3f3ec;">
            <form>
                <p v-if="errorMessage" class="error-message" style="color: red;">{{ errorMessage }}</p>
                <div class="mb-3">
                  <label for="username" class="form-label">Username</label>
                  <input v-model="username" type="username" class="form-control" id="username" aria-describedby="usernameHelp">
                  
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input v-model="password" type="password" class="form-control" id="password" aria-describedby="passwordHelp">
                  <div id="passwordHelp" class="form-text">We'll never share your personal details with anyone else.</div>
                </div>
                <button type="button" class="btn btn-primary" style="background-color: #1A2E35;" v-on:click="login">Login</button>
            </form>

        </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: '',
            errorMessage: ''
        };
    },
    methods: {
        async login() {
            try {
                // Send request to server to get token
                const response = await fetch('http://127.0.0.1:8000/api-auth/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password,
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.access) {
                        const token = data.access;
                        console.log(token);
                        // Store token in session storage
                        sessionStorage.setItem('token', token);
                        // Redirect to home page
                        this.$router.push('/');
                    } else {
                        this.errorMessage = 'Invalid credentials. Please try again.';
                    }
                } else {
                    this.errorMessage ='Login failed';
                }
            } catch (error) {
                this.errorMessage ='An error occurred during login:';
            }
        }
    }
};
</script>