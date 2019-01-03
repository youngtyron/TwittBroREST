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
                 url: this.$root.baseUrl +'api/get_id/',
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
