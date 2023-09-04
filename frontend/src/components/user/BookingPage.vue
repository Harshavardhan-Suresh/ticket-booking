<template>
  <div>
    <div class="venues1" style="flex-direction: column; align-items: center">
      <div v-if="tickets.length > 0">
        <div
          v-for="ticket in tickets"
          :key="ticket.id"
          class="card main_card"
          style="width: 18rem; margin-bottom: 20px"
        >
          <img
            :src="
              ticket.show_poster ? ticket.show_poster : '/images/no_image.png'
            "
            class="card-img-top"
            :style="
              ticket.show_poster
                ? 'background-color: white; height: 300px;'
                : 'background-color: white; height: 300px;'
            "
          />
          <div class="card-body">
            <h3 class="card-title">{{ ticket.show_name }}</h3>
            <h3 class="card-text" style="font-size: 18px">
              venue: {{ ticket.venue_name }}
            </h3>
            <h3 class="card-text" style="font-size: 18px">
              time: {{ ticket.time_and_date }}
            </h3>
            <h3 class="card-text" style="font-size: 18px">
              no of seats: {{ ticket.no_of_seats }}
            </h3>
            <h3 class="card-text" style="font-size: 18px">
              price: Rs {{ ticket.total_price.toFixed(2) }}
            </h3>
          </div>
        </div>
      </div>
      <div v-else style="text-align: center">
        <h3 class="card-text" style="font-size: 25px; font-weight: bold">
          No Tickets booked by user
        </h3>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api.js";
import jwtDecode from "jwt-decode";
export default {
  data() {
    return {
      tickets: [], // Initialize tickets as an empty array to be populated later
    };
  },
  methods: {
    async fetchData() {
      // Fetch tickets data from the API using axios or any other HTTP client
      const token = localStorage.getItem("access_token");
      if (token) {
        try {
          const decodedToken = jwtDecode(token);
          const user_id = decodedToken.sub.user_id;
          const response = await api.get(`/api/booking?user_id=${user_id}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }); // Replace with the actual API endpoint to fetch user bookings
          this.tickets = response.data.tickets; // Assign the fetched tickets data to the 'tickets' data property
        } catch (error) {
          console.error(error);
        }
      } else {
        this.$router.push("/");
      }
    },
  },
  created() {
    this.fetchData();
  },
};
</script>

<style>
/* Add your custom CSS styles here or use a separate CSS file */
/* You can also include the CSS styles from the main.css file here */
</style>
