<template>
  <div
    class="container updateShow"
    style="margin-top: 150px; margin-left: 550px"
  >
    <div class="col-md-offset-1 col-md-10">
      <div
        class="col-md-offset-3 col-md-5"
        style="background-color: lightskyblue"
        id="updateShow"
      >
        <div class="shadow">
          <h3 class="page-header text-primary" style="text-align: center">
            Update Show
          </h3>
          <form
            @submit.prevent="updateShowForm"
            autocomplete="off"
            enctype="multipart/show-data"
          >
            <div class="show-group">
              <label style="font-size: 20px">Updated Name</label>
              <input
                v-model="show.updatedName"
                type="text"
                class="show-control"
                required
              />
            </div>
            <div class="show-group">
              <label style="font-size: 20px">Updated Poster</label>
              <br />
              <input
                type="file"
                @change="onFileSelected"
                class="show-control-file"
              />
            </div>
            <div
              class="show-group"
              style="margin-top: 5px; justify-content: center"
            >
              <button
                type="submit"
                class="btn btn-primary small-btn"
                style="width: 150px; height: 50px; font-size: 25px"
              >
                Submit
              </button>
              <router-link
                to="/show"
                class="btn btn-danger small-btn"
                style="width: 150px; height: 50px; font-size: 25px"
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
      show: {
        updatedName: "",
        updatedPoster: null,
      },
    };
  },
  methods: {
    onFileSelected(event) {
      const file = event.target.files[0];
      this.show.updatedPoster = file;
    },
    async fetchData() {
      try {
        const token = localStorage.getItem("access_token");
        const showId = this.$route.params.show_id;
        if (token) {
          const response = await api.get(`/api/show/${showId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log(response.data);
          this.show.updatedName = response.data.name;
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        // Handle errors here if needed
        console.error(error);
      }
    },
    async updateShowForm() {
      try {
        const token = localStorage.getItem("access_token");
        const showId = this.$route.params.show_id;
        if (token) {
          const formData = new FormData();
          formData.append("photo", this.show.updatedPoster);
          const response = await api.post("/api/photo/add", formData, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          });
          await api.put(
            `/api/show/${showId}`,
            {
              poster: response.data.photo_path,
              name: this.show.updatedName,
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
        // Handle errors here if needed
        console.error(error);
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
