<template>
  <div class="container1">
    <div class="signup-form col-md-5 shadow">
      <h3
        class="page-header text-primary text-center"
        style="font-size: 30px; color: rgb(67, 66, 66)"
      >
        User Signup
      </h3>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <form @submit.prevent="submitForm" autocomplete="off">
        <div class="form-group">
          <label style="font-size: 20px">Username</label>
          <input
            v-model="formData.username"
            type="text"
            class="form-control"
            placeholder="Enter your username"
            minlength="4"
            maxlength="20"
            required
          />
        </div>
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
          <label style="font-size: 20px">Phone Number</label>
          <input
            v-model="formData.phone_number"
            type="tel"
            class="form-control"
            placeholder="Enter your phone number"
            minlength="10"
            maxlength="10"
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
            minlength="4"
            maxlength="20"
            required
          />
        </div>
        <div class="form-group">
          <label style="font-size: 20px">Confirm Password</label>
          <input
            v-model="formData.confirm_password"
            type="password"
            class="form-control"
            placeholder="Confirm your password"
            minlength="4"
            maxlength="20"
            required
          />
        </div>
        <div class="form-group">
          <button type="submit" class="btn btn-success button-margin">
            Signup
          </button>
          <router-link
            to="/user"
            class="btn btn-danger button-margin link-padding"
            >Login</router-link
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
      const apiUrl = "/api/user/register";
      const formData = {
        username: this.formData.username,
        phone_number: this.formData.phone_number,
        email: this.formData.email,
        password: this.formData.password,
      };
      if (this.formData.password !== this.formData.confirm_password) {
        this.error = "Passwords do not match";
        return;
      }
      try {
        const response = await api.post(apiUrl, formData);
        const { access_token } = response.data;
        this.setToken(access_token);
        this.$router.push("/user");
      } catch (e) {
        console.log(e);
        this.error = e.response.data.message;
      }
    },
    clearError() {
      this.error = null;
    },
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
.container1 {
  height: 100%;
  display: flex;
  padding: 3% !important;
  justify-content: center;
  align-items: center;
}

.signup-form {
  background-color: palegoldenrod;
  padding: 20px;
  border-radius: 5px;
}
</style>
