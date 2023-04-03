<template>
  <div id="app">
    <nav>
      <router-link to="/">Election Configuration</router-link> |
      <router-link to="/totalization">Totalization</router-link> |
      <router-link to="/voting">Voting</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<style>
#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
	/* background-image: url("./assets/voting.jpg");
	background-position: center bottom;
	background-repeat: no-repeat;
	background-size: cover; */
}

nav {
	padding: 30px;
}

nav a {
	font-weight: bold;
	color: #2c3e50;
}

nav a.router-link-exact-active {
	color: #42b983;
}
</style>
