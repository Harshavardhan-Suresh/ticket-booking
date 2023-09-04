<template>
  <div class="container updateScreen">
    <div class="col-md-offset-1 col-md-10">
      <div
        class="col-md-offset-3 col-md-5"
        style="background-color: lightskyblue"
        id="updateScreen"
      >
        <div class="shadow">
          <h3 class="page-header text-primary" style="text-align: center">
            Update Venue
          </h3>
          <form
            @submit.prevent="submitForm"
            autocomplete="off"
            enctype="multipart/form-data"
          >
            <div class="form-group">
              <label style="font-size: 20px">Updated Name</label>
              <input v-model="venue.name" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">Updated City</label>
              <input v-model="venue.city" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">Updated Address</label>
              <input v-model="venue.address" type="text" class="form-control" />
            </div>
            <div class="form-group">
              <label style="font-size: 20px">Updated Capacity</label>
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
                style="width: 150px; height: 50px; font-size: 25px"
              >
                Submit
              </button>
              <a
                class="btn btn-danger small-btn"
                style="width: 150px; height: 50px; font-size: 25px"
                href="/venue"
                >Cancel</a
              >
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
    async submitForm() {
      try {
        const token = localStorage.getItem("access_token");
        const venueId = this.$route.params.venue_id;
        if (token) {
          await api.put(`/api/venue/${venueId}`, this.venue, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.$router.push("/venue");
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        // Handle errors here if needed
        console.error(error);
      }
    },
    async fetchData() {
      try {
        const token = localStorage.getItem("access_token");
        const venueId = this.$route.params.venue_id;
        if (token) {
          const response = await api.get(`/api/venue/${venueId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.venue = response.data;
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
