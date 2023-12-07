<template>
  <Navbar></Navbar>
  <HelloWorldVue></HelloWorldVue>
  <button type="button" class="btn btn-warning">Warning</button>
</template>

<script>

import Navbar from './components/Navbar.vue';
import HelloWorldVue from './components/HelloWorld.vue';

export default {
  name: 'App',
  components: {
    Navbar,
    HelloWorldVue
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
