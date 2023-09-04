<template>
  <div>
    <nav class="navbar">
      <div class="navbar-links">
        <ul>
          <li><a href="/user/show">Movies</a></li>
          <li><a href="/user/venue">Theatres</a></li>
          <li><a href="/user/bookings">Bookings</a></li>
        </ul>
      </div>
      <div class="navbar-links-right">
        <ul>
          <li><a href="/logout">Logout</a></li>
        </ul>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<style>
.navbar {
  display: flex;
  justify-content: space-between;
  text-align: center;
  align-items: center;
  padding: 1rem;
  background-color: lightblue;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.navbar-links ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  justify-items: center;
}

.navbar-links li {
  margin: 0 1rem;
}

.navbar-links a {
  color: #000;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.2s ease-in-out;
}

.navbar-links a:hover {
  color: #f00;
}

.navbar-links-right ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  justify-items: center;
}

.navbar-links-right li {
  margin: 0 1rem;
}

.navbar-links-right a {
  color: #000;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.2s ease-in-out;
}

.navbar-links-right a:hover {
  color: #f00;
}
</style>
