<!-- frontend/src/views/FeedbackComponent.vue -->

<template>
  <div class="feedback-container">
    <h1><strong>Roll Number</strong> {{ rollNo }}</h1>
    <h1>Edit Feedback</h1>
    <form @submit.prevent="editFeedback">
      <label for="title">Title:</label>
      <input v-model="editedTitle" type="text" id="title" />
      <br>

      <label for="rating">Rating:</label>
      <input v-model="editedRating" type="text" id="rating" />
      <br>

      <label for="description">Description:</label>
      <textarea v-model="editedDescription" id="description"></textarea>
      <br>

      <button type="submit">Save Changes</button>
    </form>
  </div>
</template>
  
  
<style scoped>
.feedback-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

h1 {
  font-size: 24px;
  margin-bottom: 10px;
}

p {
  margin: 0;
}

.feedback-list {
  margin-top: 20px;
}

.feedback-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
}

.feedback-title {
  font-size: 18px;
  margin-bottom: 10px;
}

.feedback-details {
  font-size: 16px;
}

.no-feedback-message {
  margin-top: 20px;
  color: #888;
  text-align: center;
}
</style>
  
  
    
<script>

import axios from 'axios';

export default {

  data() {



    return {
      feedbackData: '',
      rollNo: '',
      courseCode: '',
      feedbackId: '',
      editedTitle: '',
      editedRating: '',
      editedDescription: '',
    };
  },
  created() {

    this.feedbackId = this.$route.params.feedbackId;

    this.callFeedback();

    this.editFeedback();

  },
  methods: {


    async callFeedback() {
      const accessToken = sessionStorage.getItem('token');



      const apiUrl = 'http://localhost:8000/course/feedback';

      try {
        // Make a GET request to the other API endpoint with the access token in the Authorization header
        console.log(1);
        const response = await axios.get(apiUrl, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            // Add any other headers if required by the API
          },
        });

        const data = response.data;
        this.feedbackData = data.feedbacks;
        const selectedFeedback = this.feedbackData.find(feedback => String(feedback.fid) === this.feedbackId);

        // Check if the feedback is found
        this.editedTitle = selectedFeedback.title;
        this.editedRating = selectedFeedback.rating;
        this.editedDescription = selectedFeedback.description;
        this.rollNo = data.roll_no;
        console.log(this.editedTitle);

      } catch (error) {
        // Handle errors
        console.error('Error:', error);
      }
    },
    async editFeedback() {


      const accessToken = sessionStorage.getItem('token');
      // URL of the other API endpoint
      const apiUrlModify = `http://localhost:8000/course/feedback/modify/${this.feedbackId}`;
      console.log(this.editedTitle);
      const postData = {
        // Include the data you want to send in the POST request
        // For example, if you are updating feedback, you might have something like:
        title: this.editedTitle,
        rating: this.editedRating,
        description: this.editedDescription,
      };
      console.log(this.editedTitle);
      try {
        // Make a GET request to the other API endpoint with the access token in the Authorization header
        console.log(1);
        const response = await axios.post(apiUrlModify, postData, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            // Add any other headers if required by the API
          },
        });
        console.log(response);
        const data = response.data;
        this.feedbackData = data;
        this.rollNo = data.roll_no;
        console.log(this.feedbackData, this.rollNo);
      } catch (error) {
        // Handle errors
        console.error('Error:', error);
      }

    },



  }
};
</script>
    