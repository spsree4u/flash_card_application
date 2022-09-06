
<template>
    <div id="app">
        <Decks/>
    </div>
</template>

<script type="module">
import Decks from "./components/decks.vue"

export default {
    name: "App",
    components: {
        Decks,
    },
}
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Ariel, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
</style>
