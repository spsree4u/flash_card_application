// import Vue from 'vue';
// import App from './App.vue';
// import Vue from 'vue';

let baseURL = "http://localhost:3000/";

Vue.config.devtools = true;
// Vue.config.productionTip = false;
// export const EventBus = new Vue();

Vue.component("app-header", {
  template: `
  <div>
    <h1>Flash Card Application</h1>
    <p><a href="/">Home</a></p>
    <p v-if="username">
      Hello {{username}}, Welcome!!
      <a href="/logout">Logout</a>
    </p>
    <p v-else>
      <a href="/login">Login</a> or <a href="/register">Register</a>
    </p>
  </div>
  `,
  props: ['username'],
});

Vue.component("decks", {
  template: `
  <div>
    <div v-if="decks_list">
      <ol>
        <li v-for="deck in decks_list">
          <div class="container-fluid" style="border:1px solid #cecece;">
          <div class="card text-white bg-dark mb-3" style="max-width: 36rem;">
            <div class="card-body">
              <h2 class="card-title">
                <a v-bind:href="'/deck/' + deck.deck_id">{{ deck["title"] }}</a>
              </h2>
              <div class="card-body">
                <h5 class="card-subtitle mb-2 text-muted">
                  Last reviewed: {{ deck["last_review_date"] }}
                </h5>
                <h4 class="card-text">Score: {{ deck["score"] }}</h4>
                <a
                  v-bind:href="'/deck/' + deck.deck_id + '/update'"
                  type="button"
                  class="card-link"
                  >Edit</a
                >
                <a
                  v-bind:href="'/deck/' + deck.deck_id + '/delete'"
                  type="button"
                  class="card-link"
                  >Remove</a
                >
              </div>
            </div>
          </div>
        </div>
      </li>
    </ol>
  </div>
  <div v-else>
    No decks available
  </div>
</div>
  `,
  data: function() {
    return {
      decks_list: []
    };
  },
  methods: {
    getDeck: function() {
      // const path = "http://localhost:3000/api/decks";
      const path = baseURL + "api/decks";
      fetch(path, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
        // body: JSON.stringify({"for": this.title, "visitor_name": this.visitor_name, "visitor_message": this.visitor_message})
      })
        .then(response => response.json())
        .then(data => {
          this.decks_list = data.decks;
          console.log("Success: ", data);
        })
        .catch(error => {
          console.error("Error: ", error);
        });
    }
  },
  created() {
    this.getDeck();
  }
});

Vue.component("add-deck", {
  template:`
  <div>
    <h2>Add a deck</h2>
    <p>Title: <input class="mb-3" type="text" v-model="deck_name"/></p>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="addDeck">Add</button>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="cancelAdd">Cancel</button>
  </div>
  `,
  data: function() {
    return {
      deck_name: ""
    }
  },
  methods: {
    addDeck: function() {
      // const path = "http://localhost:3000/api/deck";
      const path = baseURL + "api/deck";
      fetch(path, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({"title": this.deck_name})
      })
        .then(response => response.json())
        .then(data => {
          // this.decks_list = data.decks;
          // window.location.href = 'http://localhost:3000/';
          window.location.href = baseURL;
          console.log("Success: ", data);
        })
        .catch(error => {
          console.error("Error: ", error);
        });
    },
    cancelAdd: function() {
      // window.location.href = 'http://localhost:3000/';
      window.location.href = baseURL;
    }
  }
});

Vue.component("edit-deck", {
  template:`
  <div>
    <h2>Edit deck</h2>
    <p>Title: <input class="mb-3" type="text" v-model="deck_name"/></p>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="editDeck">Apply</button>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="cancelEdit">Cancel</button>
  </div>
  `,
  data: function() {
    return {
      deck_name: "",
      url_data: "",
      deck_id: 0
    }
  },
  methods: {
    editDeck: function() {
      // const path = "http://localhost:3000/api/deck/" + this.deck_id;
      const path = baseURL + "api/deck/" + this.deck_id;
      fetch(path, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({"title": this.deck_name})
      })
        .then(response => response.json())
        .then(data => {
          // this.decks_list = data.decks;
          // window.location.href = 'http://localhost:3000/';
          window.location.href = baseURL;
          console.log("Success: ", data);
        })
        .catch(error => {
          console.error("Error: ", error);
        });
    },
    cancelEdit: function() {
      // window.location.href = 'http://localhost:3000/';
      window.location.href = baseURL;
    }
  },
  created(){
    this.url_data = window.location.href;
    var fields = this.url_data.split('/');
    // console.log(fields);
    this.deck_id = fields[4];
   },
});

Vue.component("remove-deck", {
  template:`
  <div>
    <h2>Remove deck</h2>
    <div class="mt-3 mb-3">
      <label>Do you want to remove this deck? All cards in this deck will be lost!!</label>
    </div>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="removeDeck">Confirm</button>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="cancelRemove">Cancel</button>
  </div>
  `,
  data: function() {
    return {
      url_data: "",
      deck_id: 0
    }
  },
  methods: {
    removeDeck: function() {
      // const path = "http://localhost:3000/api/deck/" + this.deck_id;
      const path = baseURL + "api/deck/" + this.deck_id;
      fetch(path, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json"
        },
        // body: JSON.stringify({"title": this.deck_name})
      })
        .then(response => response.json())
        .then(data => {
          // this.decks_list = data.decks;
          // window.location.href = 'http://localhost:3000/';
          window.location.href = baseURL;
          console.log("Success: ", data);
        })
        .catch(error => {
          console.error("Error: ", error);
        });
    },
    cancelRemove: function() {
      // window.location.href = 'http://localhost:3000/';
      window.location.href = baseURL;
    }
  },
  created(){
    this.url_data = window.location.href;
    var fields = this.url_data.split('/');
    // console.log(fields);
    this.deck_id = fields[4];
   },
});

Vue.component("deck-view", {
  template:`
  <div>
    <h2>{{ deck.title }}</h2>
    <h4>Last reviewed: {{ deck.last_review_date }}</h4>
    <h4 class="mb-3">Score: {{ deck.score }}</h4>
    <div class="col-auto">
      <button class="btn btn btn-primary btn-lg mb-3" v-on:click="playGame">Play Game</button>
    </div>
    <div class="col-auto">
      <button class="btn btn btn-secondary btn-lg mb-3" v-on:click="addCard">Add a Card</button>
    </div>
    <div class="col-auto">
      <button class="btn btn-secondary btn-lg mb-3" v-on:click="searchCard">Search a Card</button>
    </div>
  </div>
  `,
  data: function() {
    return {
      deck_id: "",
      deck: ""
    }
  },
  methods: {
    playGame: function() {
      window.location.href = baseURL + 'deck/' + this.deck_id + '/card/game?';
    },
    addCard: function() {
      window.location.href = baseURL + 'deck/' + this.deck_id + '/card/create?';
    },
    searchCard: function() {
      window.location.href = baseURL + 'deck/' + this.deck_id + '/card/search?';
    }
  },
  created(){
    this.url_data = window.location.href;
    var fields = this.url_data.split('/');
    // console.log(fields);
    this.deck_id = fields[4];
    const path = baseURL + "api/deck/" + this.deck_id;
      fetch(path, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        },
      })
        .then(response => response.json())
        .then(data => {
          // window.location.href = baseURL + 'deck/' + this.deck_id;
          this.deck = data;
          console.log("Success: ", data);
        })
        .catch(error => {
          console.error("Error: ", error);
        });
   },
});

Vue.component("add-card", {
  template:`
  <div>
    <h2>Add a card</h2>
    <p>Enter a word: <input class="mb-3" type="text" v-model="word"/></p>
    <p>Enter translation: <input class="mb-3" type="text" v-model="translation"/></p>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="addCard">Add</button>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="cancelAdd">Cancel</button>
    <div class="p-2">
        <a v-bind:href="'/deck/' + deck_id">Back to deck</a>
    </div>
  </div>
  `,
  data: function() {
    return {
      deck_id: "",
      word: "",
      translation: ""
    }
  },
  methods: {
    addCard: function() {
      // const path = "http://localhost:3000/api/card";
      const path = baseURL + "api/card";
      fetch(path, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({"deck_id": this.deck_id, "word": this.word, "translation": this.translation})
      })
        .then(response => response.json())
        .then(data => {
          // this.decks_list = data.decks;
          window.location.href = baseURL + 'deck/' + this.deck_id;
          console.log("Success: ", data);
        })
        .catch(error => {
          console.error("Error: ", error);
        });
    },
    cancelAdd: function() {
      window.location.href = baseURL + 'deck/' + this.deck_id;
    }
  },
  created(){
    this.url_data = window.location.href;
    var fields = this.url_data.split('/');
    // console.log(fields);
    this.deck_id = fields[4];
   },
});

Vue.component("search-result", {
  template:`
  <div>
    <h2>Search a card</h2>
    <div v-if="card">
      <label>Here is the translation:</label>
      <h3>{{ card.translation }}</h3>
    </div>
    <div v-else>
      No card found with this word. Try another word!
    </div>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="clickNext">Next</button>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="cancelSearch">Cancel</button>
    <div class="p-2">
        <a v-bind:href="'/deck/' + deck_id">Back to deck</a>
    </div>
  </div>
  `,
  data: function() {
    return {
      deck_id: "",
      card: "",
    }
  },
  methods: {
    clickNext: function() {
      window.location.href = baseURL + 'deck/' + this.deck_id + '/card/search?';
    },
    cancelSearch: function() {
      window.location.href = baseURL + 'deck/' + this.deck_id;
    }
  },
  created(){
    this.url_data = window.location.href;
    var fields = this.url_data.split('/');
    // console.log(fields);
    this.deck_id = fields[4];
    // EventBus.$on("card", card => {console.log("hello    all", card)});
    console.log("Card info", this.card);
   },
});

Vue.component("search-card", {
  // template:`
  // <div>
  //   <h2>Search a card</h2>
  //   <p>Enter a word: <input class="mb-3" type="text" v-model="word"/></p>
  //   <button class="btn btn-secondary btn-lg mb-3" v-on:click="searchCard">Submit</button>
  //   <button class="btn btn-secondary btn-lg mb-3" v-on:click="cancelSearch">Cancel</button>
  //   <div class="p-2">
  //       <a v-bind:href="'/deck/' + deck_id">Back to deck</a>
  //   </div>
  // </div>
  // `,
  template:`
  <div>
    <h2>Search a card</h2>
    <p>Enter a word: <input class="mb-3" type="text" v-model="word"/></p>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="searchCard">Submit</button>
    <button class="btn btn-secondary btn-lg mb-3" v-on:click="cancelSearch">Cancel</button>
    <div v-if="card">
      <label>Here is the translation:</label>
      <h3>{{ card.translation }}</h3>
    </div>
    <div v-else>
      <label>Please enter a word to see the translation</label>
    </div>
    <div class="p-2">
        <a v-bind:href="'/deck/' + deck_id">Back to deck</a>
    </div>
  </div>
  `,
  data: function() {
    return {
      deck_id: "",
      word: "",
      card: ""
    }
  },
  methods: {
    searchCard: function() {
      const path = baseURL + "api/deck/" + this.deck_id + "/card/" + this.word;
      console.log(path)
      fetch(path, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
        // body: JSON.stringify({"deck_id": this.deck_id, "word": this.word, "translation": this.translation})
      })
        .then(response => response.json())
        .then(data => {
          this.card = data;
          console.log("Success: ", data);
          // EventBus.$emit("card", this.card);
          // window.location.href = baseURL + 'deck/' + this.deck_id + '/card/search-result?';
        })
        .catch(error => {
          this.card = {"translation": "No card found"};
          // console.error("Error: ", error);
        });
    },
    cancelSearch: function() {
      window.location.href = baseURL + 'deck/' + this.deck_id;
    }
  },
  created(){
    this.url_data = window.location.href;
    var fields = this.url_data.split('/');
    // console.log(fields);
    this.deck_id = fields[4];
   },
});

var app = new Vue({
  el: "#app",
  delimiters: ["${", "}"],
  data: {
    username: ""
  },
  methods: {
    getUser: function() {
      // const path = "http://localhost:3000/api/user";
      const path = baseURL + "api/user";
      fetch(path, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(response => response.json())
        .then(data => {
          this.username = data.username;
          console.log("Success: ", data);
        })
        .catch(error => {
          console.error("Error: ", error);
        });
    }
  },
  created() {
    this.getUser();
  }
  // components: {
  //   decks
  // },
  // render: h => h(decks),
});

// new Vue({
//   render: h => h(App),
// }).$mount('#app')
