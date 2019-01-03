<template>
  <div>
    <HomeSlot>
      <div class="user-info">
        <p class="user-name">{{user.first_name}} {{user.last_name}}</p>
        <img class='avatar' alt=''/>

      </div>
      <div class='central-strip' v-for='follow in follows' >
        <div :id="follow.id">
          <img v-if='follow.ava' class='follow-avatar' :src ='follow.ava' alt=''/>
          <img v-else class='follow-avatar' src ='/static/static/images/avatar.jpeg' alt=''/>
          <p class="follow-name" @click='userLink(follow.id)'>
            {{follow.first_name}} {{follow.last_name}}

          </p>
        </div>
      </div>
    </HomeSlot>
  </div>
</template>

<script>

    import HomeSlot from '@/components/Home.vue'

    export default{
      name: 'Follows',
      components: {
        HomeSlot,
      },
      data() {
        return {
          follows: '',
          user: '',
        }
      },
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           this.loadMyUser();
           this.getAva();
           this.loadFollowings();
      },
      methods: {
        loadFollowings(){
          $.ajax({
             url: this.$root.baseUrl +'api/profiles/followings/',
             type: "GET",
             success: (response) => {
                 this.follows =  response.data.data
               }
          })
        },

        loadMyUser(){
          $.ajax({
             url: this.$root.baseUrl +'api/profiles/user_news/',
             type: "GET",
             success: (response) => {
                this.user =  response.data.data

             }
          })
        },
        userLink(id){
          this.$router.push({name: 'wall', params: {id: id}})
        },
        getAva(){
          $.ajax({
             url: this.$root.baseUrl +'api/profiles/avatarnews/',
             type: "GET",
             success: (response) => {
                 var ava_url = '/static' + response.data.data
                 $(".avatar").attr("src", ava_url);
             },
             error: (response)=> {
               $(".avatar").attr("src", '/static/static/images/avatar.jpeg');
             },
          })
        },
      },
    }
</script>

<style scoped>

  .user-info{
    float: left;
  }
  .user-name{
    font-size: 150%;
    color: #039be5;
  }
  .central-strip{
    width: 60%;
    margin: auto;
  }
  .avatar{
    width: 150px;
    height: 150px;
    border-radius: 100px;
  }
  .follow-avatar{
    width: 70px;
    height: 70px;
    border-radius: 70px;
  }
  .follow-name{
    font-size: 150%;
  }
</style>
