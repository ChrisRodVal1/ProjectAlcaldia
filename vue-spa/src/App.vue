<template>
  <div id="app">
    <login v-if="!isLoggedIn" @login-success="isLoggedIn = true" />
    <dashboard v-else @logout="isLoggedIn = false" />
  </div>
</template>

<script>
import Login from './components/Login.vue';
import Dashboard from './components/Dashboard.vue';

export default {
  components: {
    Login,
    Dashboard
  },
  data() {
    return {
      isLoggedIn: false
    };
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
