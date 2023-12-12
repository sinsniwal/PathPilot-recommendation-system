<template>
    <div class=" p-3 d-flex justify-content-center align-items-center">
        <form style="padding: 30px;   background-color: #e3f3ec;">
            <p v-if="errorMessage" class="error-message" style="color: red;">{{ errorMessage }}</p>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="firstName" class="form-label">First Name</label>
                    <input v-model="firstName" type="text" class="form-control" id="firstName" aria-describedby="firstNameHelp">
                </div>
                <div class="col-md-6 mb-3">
                    <label for="lastName" class="form-label">Last Name</label>
                    <input v-model="lastName" type="text" class="form-control" id="lastName" aria-describedby="lastNameHelp">
                </div>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input v-model="username" type="username" class="form-control" id="username" aria-describedby="usernameHelp">
                </div>
                <div class="col-md-6 mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input v-model="password" type="password" class="form-control" id="password" aria-describedby="passwordHelp">
                    
                </div>
            </div>


            <div class="mb-3">
                <label for="userType" class="form-label">User Type</label>
                <select v-model="user_type" id="userType" class="form-select">
                    <option value="student">Student</option>
                    <option value="pod">Pod</option>
                </select>
            </div>
            <div v-if="user_type === 'pod'" class="mb-3">
                <div class="row">
                    <div class=" col-md-8 mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input v-model="email" type="email" class="form-control" id="email" aria-describedby="emailHelp">
                    </div>
                    <div class="col-md-4 mb-3">
                        <label for="rollNo" class="form-label">Id</label>
                        <input v-model="roll_no" type="text" class="form-control" id="rollNo" aria-describedby="rollNoHelp">
                    </div>
                </div>
            </div>
            <div v-if="user_type === 'student'" class="mb-3">
                <label for="email2" class="form-label">Email</label>
                <input v-model="email2" type="email" class="form-control" id="email2" aria-describedby="emailHelp">
            </div>
            <button type="button" class="btn btn-primary" style="background-color: #1A2E35;" v-on:click="register">Register</button>
            <p class="info-message" style="color: rgb(75, 74, 74);">If you already have an account, <a href="login">login here.</a></p>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            firstName: '',
            lastName: '',
            email: '',
            email2: '',
            password: '',
            user_type: '',
            roll_no: '',
            errorMessage: ''
        };
    },
    methods: {
        validateEmail(email) {

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        },
        validateStudentEmail(email){
            return email.endsWith('@ds.student.iitm.ac.in');
        }
        ,
        async register() {
            try {
                if (this.user_type ===''){
                    this.errorMessage='Please fill the form';
                    return;
                }
                if(this.user_type=='student' & !this.validateEmail(this.email2)){
                    this.errorMessage = "Wrong Student email format";
                    return ;
                }
                // Check if email is in correct format
                if (this.user_type=='pod' & !this.validateEmail(this.email)) {
                    this.errorMessage = 'Invalid email format';
                    return;
                }


                // Send request to server to register user
                const response = await fetch('http://127.0.0.1:8000/api-auth/register/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password,
                        first_name: this.firstName,
                        last_name: this.lastName,
                        email: this.user_type==='student' ? this.email2: this.email,
                        user_type: this.user_type,
                        roll_no: this.user_type === 'student' ? this.email2.split('@')[0] : this.roll_no
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    if (data.status == 200) {
                        if (data.access) {
                            const token = data.access;
                            console.log(token);
                            // Store token in session storage
                            sessionStorage.setItem('token', token);
                            sessionStorage.setItem('username', this.username);
                            sessionStorage.setItem('usertype',data.usertype)
                            // Redirect to home page
                            window.location.href = '/';
                        } else {
                            this.errorMessage = 'Invalid credentials. Please try again.';
                        }
                    } else {
                        if (data.message) {
                            this.errorMessage = data.message;
                        }
                    }
                } else {
                    this.errorMessage = 'Registration failed';
                }
            } catch (error) {
                this.errorMessage = 'An error occurred during registration:';
            }
        }
    }
};
</script>