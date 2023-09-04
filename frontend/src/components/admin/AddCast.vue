<template>
  <div class="container addCast" style="margin-top: 150px; margin-left: 550px">
    <div class="col-md-offset-1 col-md-10">
      <div
        class="col-md-offset-3 col-md-5"
        style="background-color: lightskyblue"
        id="addCast"
      >
        <div class="shadow">
          <form
            @submit.prevent="addCast"
            autocomplete="off"
            enctype="multipart/form-data"
          >
            <h3 class="page-header text-primary" style="text-align: center">
              Add Cast
            </h3>
            <h3 class="page-header text-primary" style="text-align: center">
              Show: {{ show.name }}
            </h3>
            <div class="form-group">
              <label style="font-size: 20px">Celebrities</label>
              <select
                v-model="selectedCelebrity.id"
                class="form-control"
                style="
                  background-color: lightyellow;
                  width: 80%;
                  margin: auto !important;
                  text-align: center;
                "
              >
                <option value="" disabled selected>Select celebrity</option>
                <option
                  v-for="celebrity in celebrities"
                  :value="celebrity.id"
                  :key="celebrity.id"
                >
                  {{ celebrity.name }}
                </option>
              </select>
            </div>
            <div
              class="form-group"
              style="margin-top: 5px; justify-content: center"
            >
              <button
                type="submit"
                class="btn btn-primary small-btn"
                style="
                  width: 150px;
                  height: 50px;
                  align-text: center;
                  font-size: 25px;
                "
              >
                Submit
              </button>
              <router-link
                to="/show"
                class="btn btn-danger small-btn"
                style="
                  width: 150px;
                  height: 50px;
                  align-text: center;
                  font-size: 25px;
                "
              >
                Cancel
              </router-link>
            </div>
          </form>
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
      selectedCelebrity: {
        id: "",
      }, // To store the selected celebrity IDs
      celebrities: [], // To store the fetched celebrity data
      show: {},
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          // Fetch the list of celebrities from your API endpoint
          // and store it in the 'celebrities' data property
          // Example: this.celebrities = await fetchCelebrities();
          const response = await api.get("/api/celebrity/all", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          const showId = this.$route.params.show_id;
          const response1 = await api.get(`/api/show/${showId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log(response.data);
          console.log(response1.data);
          this.celebrities = response.data.celebrities.filter(
            (celebrity) =>
              !response1.data.cast.some((c) => c.name === celebrity.name)
          );
          this.show = response1.data;
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error(error);
      }
    },
    async addCast() {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const showId = this.$route.params.show_id;
          await api.post(
            `/api/cast/add`,
            {
              show_id: showId,
              celebrity_id: this.selectedCelebrity.id,
            },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          this.$router.push("/show");
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style>
/* Add your CSS styles here */
</style>
