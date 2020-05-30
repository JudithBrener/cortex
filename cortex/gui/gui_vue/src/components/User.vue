<template>
  <div class="user row">
    <b-container class="align-self-center">
      <b-card :title="user.username" class="text-center">
        <b-card-text>
          <a>
            <b-icon icon="card-list"></b-icon>
            <span class="detils font-weight-bold">   User ID:</span>
            {{user_details.user_id}}
          </a>
          <br />
          <a>
            <b-icon icon="calendar-date"></b-icon>
            <span class="detils font-weight-bold">   Birthday:</span>
            {{user_details.birthday}}
          </a>
          <br />
          <a>
            <b-icon icon="arrow-left-right"></b-icon>
            <span class="detils font-weight-bold">   Gender:</span>
            {{user_details.gender}}
          </a>
          <br />
        </b-card-text>
        <b-button v-bind:href="'#/snapshots/' + user.user_id" variant="primary">
          <b-icon icon="camera"></b-icon>   Go to Snapshots
        </b-button>
      </b-card>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "User",
  props: ["user"],
  data() {
    return { user_details: {} };
  },
  created() {
    axios
      .get(this.hostUrl +"/users/" + this.user.user_id)
      .then(res => (this.user_details = res.data))
      .catch(err => console.log(err));
  }
};
</script>

<style scoped>
.detils {
  font-size: 12pt;
}

.container {
  max-width: 30%;
}

.card-text {
  text-align: justify;
}
</style>