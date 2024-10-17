<template>
  <div class="container mt-5">
    <h2>Bienvenido</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <div class="input-group">
          <i class="fas fa-user"></i>
          <input type="text" id="username" placeholder="Username..." v-model="username" class="form-control" required />
        </div>
      </div>
      <div class="form-group">
        <div class="input-group">
          <i class="fas fa-lock"></i>
          <input type="password" id="password" placeholder="Password..." v-model="password" class="form-control" required />
        </div>
      </div>
      <div class="button-group">
        <button type="submit" class="btn btn-primary">
          <i class="fas fa-sign-in-alt logo-spacing"></i> Login
        </button>
        <button type="button" class="btn btn-cancel" @click="cancel">
          <i class="fas fa-times logo-spacing"></i> Cancel
        </button>
      </div>

    </form>
    <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>

    <!-- Social Login Section -->
    <div class="social-login mt-4">
      <p>OR</p>
      <button class="btn btn-google" @click="loginWithGoogle">
        <img src="../assets/google-logo.png" alt="Google Logo" class="social-logo" />
        Continue with Google
      </button>
      <button class="btn btn-microsoft" @click="loginWithMicrosoft">
        <img src="../assets/microsoft-logo.png" alt="Microsoft Logo" class="social-logo" />
        Continue with Microsoft Account
      </button>
      <button class="btn btn-apple" @click="loginWithApple">
        <img src="../assets/apple-logo.png" alt="Apple Logo" class="social-logo" />
        Continue with Apple
      </button>
    </div>
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
    login() {
      if (this.username === 'admin' && this.password === 'admin') {
        this.$emit('login-success');
      } else {
        this.errorMessage = 'Invalid credentials. Please try again.';
      }
    },
    cancel() {
      this.username = '';
      this.password = '';
      this.errorMessage = ''; 
    },
    loginWithGoogle() {
      console.log('Logging in with Google...');
    },
    loginWithMicrosoft() {
      console.log('Logging in with Microsoft...');
    },
    loginWithApple() {
      console.log('Logging in with Apple...');
    }
  }
};
</script>

<style scoped>
.input-group {
  display: flex;
  align-items: center;
  background-color: #482778;
  border-radius: 5px;
  padding: 5px;
}

.input-group i {
  color: white;
  margin-right: 8px;
}

.logo-spacing {
  margin-right: 10px;
}

.container {
  max-width: 400px;
  background-color: #3C3C3B;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

h2 {
  color: white;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
  color: white;
}

label {
  color: #FFFFFF;
  margin-bottom: 5px;
  display: block;
  font-weight: bold;
}

.form-control {
  background-color: #482778;
  color: white;
  border: 1px solid #6D56A0;
  padding: 10px;
  border-radius: 5px;
  transition: border-color 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: #6D56A0;
  background-color: #482778;
  color: white;
}

.form-control::placeholder {
  color: white;
  opacity: 1;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.btn-primary {
  background-color: #6D56A0;
  border: none;
  color: white;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.btn-primary:hover {
  background-color: #5B4B8A;
}

.btn-cancel {
  background-color: #FF7F7F;
  border: none;
  color: white;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.btn-cancel:hover {
  background-color: #e06f6f;
}

.alert-danger {
  background-color: #FFCCCC;
  color: #D8000C;
  padding: 10px;
  border-radius: 5px;
}

.social-login {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  color: white;
}

.social-login p {
  margin: 10px 0;
}

.btn {
  display: flex;
  align-items: center;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  margin-bottom: 10px;
  color: white;
  font-weight: bold;
}

.btn-google {
  background-color: #db4437;
}

.btn-microsoft {
  background-color: #0078d4;
}

.btn-apple {
  background-color: #000;
}

.social-logo {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}

.btn-google:hover {
  background-color: #c13528;
}

.btn-microsoft:hover {
  background-color: #005a9e;
}

.btn-apple:hover {
  background-color: #333;
}
</style>


