<template>
  <div class="cele">
    <div
      v-for="celebrity in celebrities"
      :key="celebrity.id"
      class="card main_card"
      style="width: 18rem"
    >
      <div class="card-body">
        <div v-if="celebrity.photo">
          <img
            class="card-img-top"
            :src="celebrity.photo"
            alt="Card image"
            style="
              background-color: white;
              height: 90px;
              width: 90px;
              border-radius: 45px;
            "
          />
        </div>
        <div v-else>
          <svg
            class="card-img-top bi bi-person-circle"
            xmlns="http://www.w3.org/2000/svg"
            width="80"
            height="80"
            fill="currentColor"
            viewBox="0 0 16 16"
          >
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
            <path
              fill-rule="evenodd"
              d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"
            />
          </svg>
        </div>
        <h3 class="card-title">{{ celebrity.name }}</h3>
      </div>
    </div>
    <div
      class="card main_card"
      id="venue_add"
      style="
        width: 18rem;
        background-color: pink !important;
        border-color: pink !important;
        box-shadow: none;
      "
    >
      <div
        class="card-body"
        style="display: flex; justify-content: center; align-items: center"
      >
        <div class="add" style="text-align: center">
          <a
            href="/celebrity/add"
            style="
              display: inline-block;
              width: 36px;
              height: 36px;
              border-radius: 50%;
              background-color: red;
              color: black;
              font-size: 25px;
            "
            >+</a
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api.js";
export default {
  data() {
    return {
      celebrities: [], // Populate this array with your celebrity data from the backend or API
    };
  },
  methods: {
    async fetchData() {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const response = await api.get("/api/celebrity/all", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.celebrities = response.data["celebrities"];
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    this.fetchData();
  },
};
</script>

<style>
/* Add your CSS styles here */
</style>
