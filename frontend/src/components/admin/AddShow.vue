<template>
  <div class="container addShow" style="margin-top: 150px; margin-left: 550px">
    <div class="col-md-offset-1 col-md-10">
      <div
        class="col-md-offset-3 col-md-5"
        style="background-color: lightskyblue"
        id="addShow"
      >
        <div class="shadow">
          <form
            @submit.prevent="addShow"
            autocomplete="off"
            enctype="multipart/form-data"
          >
            <h3 class="page-header text-primary" style="text-align: center">
              Add Show
            </h3>
            <div class="form-group">
              <label style="font-size: 20px">Name</label>
              <input v-model="show.name" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">Poster</label>
              <br />
              <input
                type="file"
                @change="onFileSelected"
                class="form-control-file"
              />
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
      show: {
        name: "",
        poster: null,
      },
    };
  },
  methods: {
    onFileSelected(event) {
      const file = event.target.files[0];
      this.show.poster = file;
    },
    async addShow() {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const formData = new FormData();
          formData.append("photo", this.show.poster);
          const response = await api.post("/api/photo/add", formData, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          });
          await api.post(
            "/api/show/add",
            {
              poster: response.data.photo_path,
              name: this.show.name,
            },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          // console.log(response);
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
};
</script>

<style>
/* Add your CSS styles here */
</style>
