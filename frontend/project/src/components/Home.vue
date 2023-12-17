<template>
    <div class="row flex-lg-row-reverse align-items-center pt-5 gx-0 px-5">
        <div class="col-10 col-sm-8 col-lg-6 p-2">
            <img src="../assets/pic2.jpg" alt="" class="ms-2" style="width: 100%;">
        </div>
        <div v-if="token" class="col-lg-6 p-2">
            <div v-if="usertype=='student'">
                <h1 class="display-4 fw-bold text-body-emphasis lh-1 mb-2">Navigate Your Learning Journey</h1>
                <p class="lead"></p>
                <button type="button" @click="this.$router.push('/recommend')" class="btn btn-primary btn-lg mt-3 mx-auto d-block" style="background-color: #1A2E35;">Recommendation</button>
                <button type="button" @click="this.$router.push('/feedback')" class="btn btn-primary btn-lg mt-3 mx-auto d-block" style="background-color: #1A2E35;">Feedback</button>
                 </div>
            
            <div v-else-if="usertype=='pod'">
                <h1 class="display-4 fw-bold text-body-emphasis lh-1 mb-2">Navigate Your Learning Journey</h1>
                <p class="lead"></p>
                <button type="button" @click="this.$router.push('/coursestats')" class="btn btn-primary btn-lg mt-3 mx-auto d-block" style="background-color: #1A2E35;">Course Stats</button>
                <button type="button" @click="this.$router.push('/feedbackstats')" class="btn btn-primary btn-lg mt-3 mx-auto d-block" style="background-color: #1A2E35;">Feedbacks</button>
            </div>
            <div v-else>
                <h1 class="display-4 fw-bold text-body-emphasis lh-1 mb-4">Navigate Your Learning Journey</h1>
                <p class="lead pt-4">Embark on a personalized educational expedition with our innovative platform. We guide you through a curated sequence of courses, unlocking a strategic roadmap tailored to your academic ambitions. Explore a seamless learning experience, where each byte of knowledge builds a foundation for your success. Navigate, discover, and excel with precision in every step of your educational journey.</p>
            </div>
           
        </div>
        <div v-else class="col-lg-6 p-2">
            <h1 class="display-4 fw-bold text-body-emphasis lh-1 mb-4">Navigate Your Learning Journey</h1>
            <p class="lead pt-4">Embark on a personalized educational expedition with our innovative platform. We guide you through a curated sequence of courses, unlocking a strategic roadmap tailored to your academic ambitions. Explore a seamless learning experience, where each byte of knowledge builds a foundation for your success. Navigate, discover, and excel with precision in every step of your educational journey.</p>
            <button type="button" @click="this.$router.push('/login')" class="btn btn-primary btn-lg mt-5 mx-auto d-block" style="background-color: #1A2E35;">Get Started</button>
        </div>
    </div>
</template>
<script>

export default {


    data() {
    return {
      token:'',
      username:'',
      usertype:'',
    };
  },

  mounted() {
    this.token=sessionStorage.getItem('token')
    this.usertype= sessionStorage.getItem("usertype")
  },}
</script>
