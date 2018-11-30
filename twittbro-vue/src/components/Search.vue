<template>
  <div>
    <HomeSlot>
      <div>
        Search
        <div v-for='post in posts' :value="post.id">
          <p>{{post.author.first_name}} {{post.author.last_name}}</p>
          <p>{{post.text}}</p>
          <p>{{post.pub_date}}</p>
          <i v-if = 'post.red' class="fas fa-heart fa-2x liking-heart red-heart" @click='likePost'>{{post.likes_quanity}}</i>
          <i v-else class="far fa-heart fa-2x liking-heart" @click='likePost'>{{post.likes_quanity}}</i>
        </div>
      </div>
    </HomeSlot>
  </div>
</template>

<script>

    import HomeSlot from '@/components/Home.vue'

    export default{
      name: 'Search',
      props: {
          text: '',
      },
      data() {
        return {
          posts: '',
        }
      },
      components: {
        HomeSlot,
      },
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           this.loadResults();
       },
      methods: {
        loadResults(){
              $.ajax({
                 url: 'http://127.0.0.1:8000/api/profiles/load_results/',
                 type: "GET",
                 data: {
                   text: this.$route.params.text
                 },
                 success: (response) => {
                   this.posts = response.data.data
                   alert('WORK')
                 }
              })
        }
      },
    }
</script>

<style scoped>
  .liking-heart{
    float: left;
  }
  .red-heart{
    color: crimson;
  }
</style>
