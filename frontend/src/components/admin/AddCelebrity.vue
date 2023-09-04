<template>
  <div
    class="container addCelebrity"
    style="margin-top: 150px; margin-left: 550px"
  >
    <div class="col-md-offset-1 col-md-10">
      <div
        class="col-md-offset-3 col-md-5"
        style="background-color: lightskyblue"
        id="addCelebrity"
      >
        <div class="shadow">
          <form
            @submit.prevent="addCelebrity"
            autocomplete="off"
            enctype="multipart/form-data"
          >
            <h3 class="page-header text-primary" style="text-align: center">
              Add Celebrity
            </h3>
            <div class="form-group">
              <label style="font-size: 20px">Name</label>
              <input
                v-model="celebrity.name"
                type="text"
                class="form-control"
                required
              />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">Photo</label>
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
                to="/celebrity"
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
      celebrity: {
        name: "",
        photo: null,
      },
    };
  },
  methods: {
    onFileSelected(event) {
      const file = event.target.files[0];
      // Update the celebrity.photo data property with the selected file
      this.celebrity.photo = file;
    },
    async addCelebrity() {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          console.log(this.celebrity.photo);
          const formData = new FormData();
          formData.append("photo", this.celebrity.photo);
          const response = await api.post("/api/photo/add", formData, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          });
          const response1 = await api.post(
            "/api/celebrity/add",
            {
              photo: response.data.photo_path,
              name: this.celebrity.name,
            },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          console.log(response1);
          this.$router.push("/celebrity");
          // Handle the API response as needed
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
