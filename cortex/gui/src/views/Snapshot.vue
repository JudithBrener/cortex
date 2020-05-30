<template>
  <div class="snapshot">
    <h2>Snapshot details:</h2>
    <h5>Snapshot ID: {{snapshot_id}}</h5>
    <h5>Datetime: {{snapshot.datetime}}</h5>
    <b-list-group v-bind:key="result_name" v-for="result_name in snapshot.results_names">
      <b-list-group-item
        v-bind:href="'#/snapshots/'+ user_id + '/' + snapshot._id + '/' + result_name"
      >{{result_name}}</b-list-group-item>
    </b-list-group>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  name: "Snapshot",
  data() {
    return {
      snapshot: {}
    };
  },
  props: ["user_id", "snapshot_id"],
  created() {
    axios
      .get(this.hostUrl +"/users/" + this.user_id + "/snapshots/" + this.snapshot_id)
      .then(res => (this.snapshot = res.data))
      .catch(err => console.log(err));
  }
};
</script>

<style scoped>

</style>
