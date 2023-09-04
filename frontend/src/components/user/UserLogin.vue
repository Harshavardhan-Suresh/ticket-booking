<template>
  <div class="container">
    <div class="login-form col-md-5 shadow">
      <h3
        class="page-header text-primary text-center"
        style="font-size: 30px; color: rgb(67, 66, 66)"
      >
        User Login
      </h3>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <form @submit.prevent="submitForm" autocomplete="off">
        <div class="form-group">
          <label style="font-size: 20px">Email</label>
          <input
            v-model="formData.email"
            type="email"
            class="form-control"
            placeholder="Enter your email"
            required
          />
        </div>
        <div class="form-group">
          <label style="font-size: 20px">Password</label>
          <input
            v-model="formData.password"
            type="password"
            class="form-control"
            placeholder="Enter your password"
            required
          />
        </div>
        <div class="form-group">
          <button type="submit" class="btn btn-success button-margin">
            Login
          </button>
          <router-link
            to="/user/signup"
            class="btn btn-danger button-margin link-padding"
            >Signup</router-link
          >
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import api from "../../api.js";

export default {
  data() {
    return {
      formData: {
        email: "",
        password: "",
      },
      error: null,
    };
  },
  methods: {
    ...mapActions(["setToken"]),
    async submitForm() {
      const apiUrl = "/api/user/login"; // Replace with your API endpoint URL
      const formData = {
        email: this.formData.email, // Replace with actual form data
        password: this.formData.password, // Replace with actual form data
      };
      try {
        const response = await api.post(apiUrl, formData);
        const { access_token } = response.data;
        localStorage.setItem("access_token", access_token);
        this.setToken(access_token);
        this.$router.push("/user/show");
      } catch (e) {
        this.error = e.response.data.message;
      }
    },
    clearError() {
      this.error = null;
    },
  },
  created() {
    localStorage.clear();
  },
  watch: {
    error() {
      if (this.error) {
        setTimeout(this.clearError, 3000);
      }
    },
  },
};
</script>

<style>
html,
body {
  height: 100%;
  padding: 0;
}

.container {
  height: 100%;
  display: flex;
  padding-top: 10% !important;
  justify-content: center;
  align-items: center;
}

.login-form {
  background-color: palegoldenrod;
  padding: 20px;
  border-radius: 5px;
}

.page-header {
  margin-bottom: 20px;
}

.form-group {
  margin-top: 15px;
}
.button-margin {
  margin-right: 20px;
}

.btn {
  width: 150px;
  height: 50px;
}
.link-padding {
  padding-top: 10px !important;
}
input {
  margin: auto !important;
  text-align: center !important;
  width: 80% !important;
  background-color: lightgoldenrodyellow !important;
}
label {
  margin-bottom: 10px !important;
}
.alert {
  color: red;
}
</style>
