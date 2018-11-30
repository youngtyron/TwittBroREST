<template>
  <div>
  </div>
</template>

<script>

    export default{
      name: 'MyWall',
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           this.redirectWall()
       },
      methods: {
        redirectWall(){
              $.ajax({
                 url: 'http://127.0.0.1:8000/api/get_id/',
                 type: "GET",
                 success: (response) => {
                   this.$router.push({name: 'wall', params: {id: response.data.id}})
                 }
              })
        }
      },
    }
</script>

<style scoped>

</style>
