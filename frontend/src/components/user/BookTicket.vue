<template>
  <div>
    <div
      class="container bookticket"
      style="margin-top: 120px; margin-left: 550px"
    >
      <div class="col-md-offset-1 col-md-10">
        <div class="col-md-offset-3 col-md-5 card main_card" id="bookTicket1">
          <div class="shadow">
            <form
              autocomplete="off"
              enctype="multipart/form-data"
              @submit.prevent="bookTicket"
            >
              <h3 class="page-header text-primary text-center">Book Ticket</h3>
              <h3 class="page-header text-primary text-center">
                Venue: {{ venue.name }}
              </h3>
              <h3 class="page-header text-primary text-center">
                Show: {{ show.name }}
              </h3>
              <div class="form-group">
                <label style="font-size: 25px">Price</label>
                <input :value="formattedPrice" class="form-control" readonly />
              </div>
              <div class="form-group">
                <label style="font-size: 25px">Available Seats</label>
                <input :value="availableSeats" class="form-control" readonly />
              </div>
              <div class="form-group">
                <label style="font-size: 25px">No of seats</label>
                <input
                  v-model="formData.no_of_seats"
                  type="number"
                  class="form-control"
                  :min="1"
                  :max="this.availableSeats"
                  required
                />
              </div>
              <div
                class="form-group"
                style="margin-top: 5px; justify-content: center"
              >
                <button
                  type="submit"
                  class="btn btn-success"
                  style="
                    width: 150px;
                    height: 50px;
                    text-align: center;
                    font-size: 25px;
                  "
                >
                  Book
                </button>
                <a
                  class="btn btn-danger"
                  style="
                    margin-left: 20px;
                    width: 150px;
                    height: 50px;
                    text-align: center;
                    font-size: 25px;
                  "
                  href="/user/show"
                  >Cancel</a
                >
              </div>
            </form>
          </div>
        </div>
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
      formData: {
        no_of_seats: 1,
      },
      venue: {},
      show: {},
      available_seats: 0,
      screen: {},
    };
  },
  computed: {
    formattedPrice() {
      return Math.round(this.screen.price * 100) / 100;
      //   return `${this.screen.price.toFixed(2)}`;
    },
    availableSeats() {
      return this.available_seats;
    },
  },
  methods: {
    async bookTicket() {
      const token = localStorage.getItem("access_token");
      if (token) {
        const apiUrl = "/api/ticket/add";
        const decodedToken = jwtDecode(token);
        const user_id = decodedToken.sub.user_id;
        const data = {
          no_of_seats: this.formData.no_of_seats,
          screen_id: this.screen.id,
          user_id: user_id,
        };
        try {
          await api.post(apiUrl, data, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.$router.push("/user/show");
        } catch (error) {
          console.error(error);
        }
      } else {
        this.$router.push("/");
      }
    },
    async fetchData() {
      const token = localStorage.getItem("access_token");
      if (token) {
        const screenId = this.$route.params.screen_id; // Replace with the actual screen ID you want to fetch
        let apiUrl = `/api/screen/${screenId}`;
        try {
          let response = await api.get(apiUrl, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.screen = response.data;
          apiUrl = `/api/venue/${this.screen.venue_id}`;
          response = await api.get(apiUrl, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.venue = response.data;
          apiUrl = `/api/show/${this.screen.show_id}`;
          response = await api.get(apiUrl, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.show = response.data;
          apiUrl = `/api/seat/available?screen_id=${screenId}`;
          response = await api.get(apiUrl, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.available_seats = response.data.available_seats;
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
.bookticket,
.addVenue,
.addCelebrity,
.addScreen,
.addShow,
.addTag,
.addCast,
.updateShow,
.updateVenue,
.updateScreen {
  /* /* margin: 0 !important; */
  margin-left: 200px !important;
  margin-top: 0 !important;
  padding-top: 0 !important;
  max-width: 85% !important;
  /* padding-left: 32% !important; */
}
#bookTicket1,
#addVenue,
#addCelebrity,
#addScreen,
#addCast,
#addTag,
#addShow,
#updateShow,
#updateScreen,
#updateVenue {
  margin-left: 300px;
}
.btn {
  margin-top: 5px !important;
}
</style>
