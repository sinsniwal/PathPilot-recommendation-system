<!-- frontend/src/views/FeedbackComponent.vue -->

<template>
  <div class="feedback-container">
    <h1><strong>Feedback for </strong> {{ courseName }}</h1>
    <p>Course ID{{ courseCode }}</p>
    <div v-if="feedbackData.feedbacks && feedbackData.feedbacks.length > 0" class="feedback-list">
      <div v-for="feedback in feedbackData.feedbacks" :key="feedback.id" class="feedback-item">
        <!-- Customize this part based on the structure of your feedback data -->
        <p><strong>Title:</strong> {{ feedback.title }}</p>
        <p><strong>Rating:</strong> {{ feedback.rating }}</p>
        <p><strong>Description:</strong> {{ feedback.description }}</p>
        <!-- Add more fields as needed -->
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

  

  export default {
    //name: 'HomeView',
    //components: {
    //FeedbackComponent
  //},
    data() {
      return {
        courseCode: '',
        feedbackData: '',
        courseName: '',
      };
    },
    created() {
      // Access the course_code parameter from the route
      this.courseCode = this.$route.params.course_code;
  
      // Fetch feedback data using the course_code
      this.fetchFeedback();
    },
    methods: {
      async fetchFeedback() {
        try {
          const response = await fetch(`http://localhost:8000/course/feedback/${this.courseCode}`);
          const data = await response.json();
          this.feedbackData = data;
          this.courseName = data.course_name;
          console.log(this.feedbackData);
        } catch (error) {
          console.error('Error fetching feedback:', error);
          this.feedbackData = 'Error fetching feedback.';
        }
      },
    },
  };
  </script>
  