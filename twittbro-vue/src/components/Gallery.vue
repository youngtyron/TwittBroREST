<template>
  <div>
      <mu-dialog :esc-press-close="false" :overlay-close="false" :open.sync="GalleryWindow">
        <div id='gallery-div'>
        <i class="fas fa-arrow-circle-left fa-2x" @click = 'previousImage'></i>
          <img class = 'gallery-image'  :src="this.$root.currentUrl" alt="image">
        <i class="fas fa-arrow-circle-right fa-2x" @click= 'nextImage'></i>
        </div>
      </mu-dialog>
  </div>
</template>

<script>



    export default{
      name: 'Gallery',
      components:{
      },

      data() {
        return {
          GalleryWindow: true,
          index: '',
        }
      },
      created(){
        this.countIndex(),
        window.addEventListener('click', this.closeListener);
        window.addEventListener('keypress', this.keyListener);
      },
      methods: {
        keyListener(event){
          if (event.keyCode == 37){
            this.previousImage()
          }
          else if (event.keyCode == 39){
            this.nextImage()
          }
          else{
            return null
          }
        },
        countIndex(){
          var index = this.$root.galleryUrls.indexOf(this.$root.currentUrl)
        },
        closeListener(e){
          var div = $("#gallery-div"); // тут указываем ID элемента
          var image = $('.one-image');
      		if (!div.is(e.target) // если клик был не по нашему блоку
      		    && div.has(e.target).length === 0
              && !image.is(e.target)) { // и не по его дочерним элементам
      			this.$root.openGallerySlot = false; // скрываем его
            this.$root.currentUrl = ''
            this.$root.galleryUrls = ''
      		}
        },
        previousImage(){
          var curr = this.$root.galleryUrls.indexOf(this.$root.currentUrl)
          var prev = curr - 1
          if (prev < 0){
            var prev = this.$root.galleryUrls.length - 1
          }
          else {
            var prev = curr - 1
          }
          this.$root.currentUrl = this.$root.galleryUrls[prev]
        },
        nextImage(){
          var curr = this.$root.galleryUrls.indexOf(this.$root.currentUrl)
          var next = curr + 1
          if (next < this.$root.galleryUrls.length){
            var next = curr + 1
          }
          else {
            var next = 0
          }
          this.$root.currentUrl = this.$root.galleryUrls[next]
        },
      },
    }
</script>

<style scoped>

.fa-arrow-circle-left{
  position: fixed;
	top: 50%;
  z-index: 101!important;
}
.fa-arrow-circle-right{
  vertical-align: middle;
}
</style>
