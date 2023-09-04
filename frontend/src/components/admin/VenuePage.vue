<template>
  <div>
    <div class="venues">
      <div
        v-for="venue in venues"
        :key="venue.id"
        class="card main_card"
        style="width: 18rem"
      >
        <div class="card-body">
          <h3 class="card-title">{{ venue.name }}</h3>
          <div
            v-for="screen in venue.screens"
            :key="screen.id"
            class="card"
            style="width: 14rem"
          >
            <div class="card-body">
              <h3 class="card-title">{{ screen.show }}</h3>
              <p class="card-text">
                {{ screen.timing }}<br />Rs: {{ screen.price }}
              </p>
              <router-link :to="`/screen/update/${screen.id}`"
                ><button class="btn btn-success small-btn">Edit</button>
              </router-link>
              <button
                @click="deleteScreen(screen.id)"
                class="btn btn-danger small-btn"
              >
                Delete
              </button>
            </div>
          </div>
          <div class="add" style="text-align: center">
            <router-link
              :to="`/screen/add/${venue.id}`"
              style="
                display: inline-block;
                width: 36px;
                height: 36px;
                border-radius: 50%;
                background-color: red;
                color: black;
                font-size: 25px;
              "
              >+</router-link
            >
          </div>
          <router-link :to="`/venue/update/${venue.id}`"
            ><button class="btn btn-primary small-btn">
              Edit
            </button></router-link
          >
          <button
            @click="deleteVenue(venue.id)"
            class="btn btn-warning small-btn"
          >
            Delete
          </button>
          <button
            @click="exportExcel(venue.id)"
            class="btn btn-light small-btn"
          >
            Export Excel
          </button>
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
            <router-link
              to="/venue/add"
              style="
                display: inline-block;
                width: 36px;
                height: 36px;
                border-radius: 50%;
                background-color: red;
                color: black;
                font-size: 25px;
              "
              >+</router-link
            >
          </div>
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
      venues: [], // You can fetch this data from the API or set it dynamically
    };
  },
  methods: {
    async fetchData() {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const response = await api.get("/api/venue/admin", {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          });
          this.venues = response.data["venues"];
          console.log(this.venues);
        }
      } catch (error) {
        console.log(error);
      }
    },
    async exportExcel(theatreId) {
      try {
        const response = await api.get(`/generate_excel/${theatreId}`, {
          responseType: "blob", // Set the response type to 'blob'
        });

        if (response.status === 200) {
          // Create a Blob URL for the Excel file
          const blob = new Blob([response.data], {
            type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          });
          const blobUrl = URL.createObjectURL(blob);

          // Create a link element and click it to initiate download
          const link = document.createElement("a");
          link.href = blobUrl;
          link.download = `theatre_${theatreId}_info.xlsx`;
          link.click();

          // Revoke the Blob URL after download
          URL.revokeObjectURL(blobUrl);
        } else {
          console.error("Excel download failed");
        }
      } catch (error) {
        console.error("Error downloading Excel:", error);
      }
    },
    async deleteVenue(venueId) {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          await api.delete(`/api/venue/${venueId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.fetchData();
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error(error);
      }
    },
    async deleteScreen(screenId) {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          await api.delete(`/api/screen/${screenId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.fetchData();
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error(error);
      }
    },
    formatTiming() {
      this.venues.forEach((venue) => {
        venue.screens.forEach((screen) => {
          const timingDate = new Date(screen.timing);
          const formattedTiming = timingDate.toLocaleString("en-US", {
            day: "numeric",
            month: "long",
            year: "numeric",
            hour: "numeric",
            minute: "numeric",
            hour12: true,
          });
          screen.timing = formattedTiming;
        });
      });
    },
  },
  created() {
    this.fetchData();
    this.formatTiming();
  },
};
</script>

<style>
.small-btn {
  width: fit-content !important;
  margin-left: 10px;
}
</style>
