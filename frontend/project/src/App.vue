<template>
  <Navbar></Navbar>
  <Home></Home>
</template>

<script>

import Navbar from './components/Navbar.vue';
import Home from './components/Home.vue';

export default {
  name: 'App',
  components: {
    Navbar,
    Home
  }
}
</script>

<style>
#app {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
