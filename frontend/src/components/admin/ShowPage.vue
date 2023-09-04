<template>
  <div class="shows">
    <div
      v-for="show in shows"
      :key="show.id"
      class="card main_card"
      style="width: 18rem"
    >
      <div v-if="show.poster">
        <img
          class="card-img-top"
          :src="show.poster"
          alt="Card image"
          style="background-color: white; height: 300px"
        />
      </div>
      <div v-else>
        <img
          class="card-img-top"
          src="/images/no_image.png"
          alt="Card image"
          style="background-color: white; height: 300px"
        />
      </div>
      <div class="card-body">
        <h3 class="card-title">
          {{ show.name }}
          <br />
          <div class="tag-buttons">
            <button
              v-for="tag in show.tags"
              :key="tag.id"
              class="tag-button"
              @click="handleTagClick(tag, show)"
            >
              {{ tag.name }}
            </button>
          </div>
          <br />
        </h3>
        <div class="add" style="text-align: center">
          <a
            :href="`/tag/add/${show.id}`"
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
        <h3 class="card-title">
          <span v-if="show.rating">
            {{ show.rating.toFixed(2) }}/10
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="25"
              height="25"
              fill="yellow"
              class="bi bi-star-fill"
              viewBox="0 0 25 25"
            >
              <path
                d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"
              />
            </svg>
          </span>
        </h3>

        <h4>Cast</h4>
        <div
          v-for="celebrity in show.cast"
          :key="celebrity.id"
          class="card"
          style="width: 12rem"
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
            <button
              @click="deleteCast(celebrity.id, show.id)"
              class="btn btn-danger small-btn"
            >
              Delete
            </button>
          </div>
        </div>
        <div class="add" style="text-align: center">
          <a
            :href="`/cast/add/${show.id}`"
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
        <router-link :to="`/show/update/${show.id}`"
          ><button class="btn btn-primary small-btn">Edit</button></router-link
        >
        <button @click="deleteShow(show.id)" class="btn btn-warning small-btn">
          Delete
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
          <a
            href="/show/add"
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
      shows: [], // Populate this array with your shows data from the backend or API
    };
  },
  methods: {
    async handleTagClick(tag, show) {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const filteredTags = show.tags.filter((t) => t.id != tag.id);
          console.log(filteredTags);
          console.log(tag);
          await api.put(
            `/api/show/${show.id}`,
            { tags: filteredTags },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          this.fetchData();
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error(error);
      }
    },
    async deleteCast(celebrity_id, show_id) {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          await api.delete(`/api/cast/${show_id}/${celebrity_id}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.fetchData();
        }
      } catch (error) {
        console.error(error);
      }
    },

    async deleteShow(show_id) {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          await api.delete(`/api/show/${show_id}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.fetchData();
        }
      } catch (error) {
        console.error(error);
      }
    },

    async fetchData() {
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const response = await api.get(`/api/show/all`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log(response);
          this.shows = response.data.shows;
        }
      } catch (error) {
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
