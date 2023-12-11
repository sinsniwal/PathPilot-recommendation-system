<!-- frontend/src/views/FeedbackComponent.vue -->

<template>
  <div class="feedback-container">
    <button @click="addFeedback()">Add New Feedback</button>
    <h1><strong>Roll Number</strong> {{ rollNo }}</h1>
    <div v-if="feedbackData.feedbacks && feedbackData.feedbacks.length > 0" class="feedback-list">
      <div v-for="feedback in feedbackData.feedbacks" :key="feedback.id" class="feedback-item">
        <!-- Customize this part based on the structure of your feedback data -->
        <p><strong>Title:</strong> {{ feedback.title }}</p>
        <p><strong>Course code:</strong> {{ feedback.course_code }}</p>
        <p><strong>Rating:</strong> {{ feedback.rating }}</p>
        <p><strong>Description:</strong> {{ feedback.description }}</p>

        <!-- Add an Edit button -->
        <button @click="editFeedback(feedback.fid)">Edit</button>
        <button @click="deleteFeedback(feedback.fid)">Delete</button>
      </div>
    </div>
    <div v-else class="no-feedback-message">
      <p>No feedback available for this course.</p>
    </div>
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
    };
  },
  created() {

    this.studentFeedback();
  },
  methods: {
    async studentFeedback() {
      const accessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyMTM4Mzk3LCJpYXQiOjE3MDIxMzExODIsImp0aSI6IjA1YmQ5Y2JiMTlkMzQxMzFiODY4MjhiZDdiMDQ3YWRhIiwidXNlcl9pZCI6Mn0.lcUlcpK9HPemUcun6ZctzJKwDnnQkDUaCo1p_K7-NQY';

      // URL of the other API endpoint
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
        this.feedbackData = data;
        this.rollNo = data.roll_no;
        console.log(this.feedbackData, this.rollNo);
      } catch (error) {
        // Handle errors
        console.error('Error:', error);
      }
    },


    addFeedback() {
      this.$router.push(`/course/post/feedback/`);
    },

    editFeedback(feedbackId) {
      // Handle the edit action here, for example, navigate to an edit page
      // You can use a router push or any other method to navigate to the edit page

      this.$router.push(`/course/feedback/modify/${feedbackId}`);
    },


    async deleteFeedback(feedbackId) {
      const accessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyMTIzNTYyLCJpYXQiOjE3MDIxMTYzNDgsImp0aSI6IjcyNjI0NWMzZjE5YjQ4MzM5ZjdjYTBmMWRjMzg3YTYwIiwidXNlcl9pZCI6Mn0.hPf92wR6vQ6r8Mc19J72GjuE6pCkQUonhgjdUAZPHjY';



      const apiUrl = `http://localhost:8000/course/feedback/modify/${feedbackId}`;

      try {
        // Make a GET request to the other API endpoint with the access token in the Authorization header
        console.log(1);
        const response = await axios.delete(apiUrl, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            // Add any other headers if required by the API
          },
        });
        console.log(response);
        this.studentFeedback();
      } catch (error) {
        // Handle errors
        console.error('Error:', error);
      }
    },

  },
};
</script>
    