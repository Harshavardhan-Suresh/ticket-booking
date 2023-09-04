<template>
  <div class="container addVenue">
    <div class="col-md-offset-1 col-md-10">
      <div
        class="col-md-offset-3 col-md-5"
        style="background-color: lightskyblue"
        id="addVenue"
      >
        <div class="shadow">
          <form
            @submit.prevent="addVenue"
            autocomplete="off"
            enctype="multipart/form-data"
          >
            <h3 class="page-header text-primary" style="text-align: center">
              Add Venue
            </h3>
            <div class="form-group">
              <label style="font-size: 20px">Name</label>
              <input v-model="venue.name" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">City</label>
              <input v-model="venue.city" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">Address</label>
              <input v-model="venue.address" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">Capacity</label>
              <input
                v-model="venue.capacity"
                type="number"
                class="form-control"
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
                to="/venue"
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
      venue: {
        name: "",
        city: "",
        address: "",
        capacity: null,
      },
    };
  },
  methods: {
    async addVenue() {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const apiUrl = "/api/venue/add";
          await api.post(apiUrl, this.venue, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.$router.push("/venue");
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style>
/* Add your CSS styles here */
</style>
