<template>
  <header class="header">
    <nav>
      <a class="nav-link" @click="aboutUs">FAQ</a>
      <a class="nav-link" @click="logout">Cerrar Sesion</a>
    </nav>
  </header>
</template>

<script>
export default {
  methods: {
    aboutUs() {
      
    },
    downloadPDF() {
      alert('Download PDF functionality not implemented.');
    },
    logout() {
      this.$emit('logout');
    }
  }
};
</script>

<style scoped>
.header {
  background-color: #6F565F;
  color: white;
  padding: 15px;
  text-align: center;
  border-bottom: 3px solid #6D56A0;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

nav {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.nav-link {
  color: white;
  text-decoration: none;
  margin: 0 15px;
  font-weight: 600;
  transition: color 0.3s;
  cursor: pointer;
}

.nav-link:hover {
  color: #482778;
  text-decoration: underline;
}

body {
  margin-top: 70px;
}
</style>

