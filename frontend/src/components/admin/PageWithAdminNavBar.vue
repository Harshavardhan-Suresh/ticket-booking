<template>
  <div>
    <nav class="navbar">
      <div class="navbar-links">
        <ul>
          <li><a href="/show">Movies</a></li>
          <li><a href="/venue">Theatres</a></li>
          <li><a href="/celebrity">Celebrity</a></li>
          <li><a href="/statistics">Statistics</a></li>
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

<style></style>
