<template>
  <Navbar></Navbar>
  <router-view></router-view>
</template>

<script>

import Navbar from './components/Navbar.vue';

export default {
  name: 'App',
  components: {
    Navbar,
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
