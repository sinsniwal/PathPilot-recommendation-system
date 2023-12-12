<template>
    <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #84caa6" id="mynavbar">
        <a class="navbar-brand" href="#" style="font-family: 'Courgette', cursive; font-size: 1.5rem">PathPilot✈️</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div v-if="username"  class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav ms-auto">
            <a class="nav-item nav-link active" href="#">Home</a>
            <a class="nav-item nav-link" @click="logout">Logout</a>
            <a class="nav-item nav-link" href="#">{{ username }}</a>
            <a class="nav-item nav-link" href="#">Help</a>
            <a class="nav-item nav-link" href="#">FAQ</a>
          </div>
        </div>
        <div v-else class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav ms-auto">
            <a class="nav-item nav-link active" href="#">Home</a>
            <a class="nav-item nav-link" href="login">Login</a>
            <a class="nav-item nav-link" href="register">Register</a>
            <a class="nav-item nav-link" href="#">Help</a>
            <a class="nav-item nav-link" href="#">FAQ</a>
          </div>  
        </div>
      </nav>
</template>

<script>
export default {
  data() {
    return {
      token:'',
      username:''
    };
  },

  mounted() {
    this.token = sessionStorage.getItem('token');
    if (this.token) {
      this.username=sessionStorage.getItem('username');
    }
  },
  methods: {
    logout() {
      sessionStorage.removeItem('token'); // Remove token from session storage
      this.token = ''; // Clear token in component data
      this.username = ''; // Clear username in component data
    }
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Courgette&display=swap');

#mynavbar {
    padding: 0.6rem 4.5rem;
    margin-bottom: 3.8rem;
    max-height: 4.5rem;
}

</style>