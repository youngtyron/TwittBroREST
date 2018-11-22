<template>
  <div>

    <div v-for='post in posts'>
      <p>{{post.author.first_name}} {{post.author.last_name}}</p>
      <p>{{post.text}}</p>
      <p>{{post.pub_date}}</p>
    </div>
  </div>
</template>

<script>

    import HomeSlot from '@/components/Home.vue'

    export default{
      name: 'Wall',
      components: {
        HomeSlot,
      },
      data() {
        return {
          posts: '',
        }
      },
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           this.loadPosts()
       },
      methods: {
        loadPosts() {
            // $.ajaxSetup({
            //     headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
            // });
            $.ajax({
               url: 'http://127.0.0.1:8000/api/profiles/posts/' + this.$route.params.id,
               type: "GET",
               success: (response) => {
                   this.posts = response.data.data
               }
            })
          },
      },
    }
</script>

<style scoped>

</style>
