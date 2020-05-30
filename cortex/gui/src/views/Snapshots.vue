<template>
  <div class="snapshots">
    <h2>Snapshots:</h2>
    <h5>User ID: {{user_id}}</h5>
    <b-list-group v-bind:key="snapshot._id" v-for="snapshot in snapshots">
      <b-list-group-item
        v-bind:href="'#/snapshots/'+ user_id + '/' + snapshot._id"
      >{{snapshot.datetime}}</b-list-group-item>
    </b-list-group>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  name: "Snapshots",
  data() {
    return {
      snapshots: []
    };
  },
  props: ["user_id"],
  created() {
    function compare(a, b) {
      if (a.datetime < b.datetime) {
        return -1;
      }
      if (a.datetime > b.datetime) {
        return 1;
      }
      return 0;
    }
    this.snapshots.sort(compare);

    axios
      .get(this.hostUrl +"/users/" + this.user_id + "/snapshots")
      .then(res => (this.snapshots = res.data))
      .catch(err => console.log(err));
  }
};
</script>
