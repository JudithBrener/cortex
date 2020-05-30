<template>
  <div class="users">
    <div v-bind:key="user.user_id" v-for="user in users">
      <User v-bind:user="user"/>
    </div>
  </div>
</template>


<script>
import User from '@/components/User.vue'
import axios from 'axios'


export default {
  name: "Users",
  data() {
    return {
      users: [
        { user_id: "1234", username: "Judith Brener" },
        { user_id: "fnklw", username: "Dan G" }
      ]
    };
  },
  components: {
    User
  },
  created() {
    axios.get('https://jsonplaceholder.typicode.com/users')
    .then(res => this.users = res.data)
    .catch(err => console.log(err))
  }
};
</script>
