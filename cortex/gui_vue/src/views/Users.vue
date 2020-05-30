<template>
  <div class="users">
    <div v-bind:key="user.user_id" v-for="user in users">
      <User v-bind:user="user" />
    </div>
  </div>
</template>


<script>
import User from "@/components/User.vue"
import axios from "axios"

export default {
  name: "Users",
  data() {
    return {
      users: []
    };
  },
  components: {
    User
  },
  created() {
    axios.get(this.hostUrl + "/users")
      .then(res => (this.users = res.data))
      .catch(err => console.log(err));
  }
};
</script>
