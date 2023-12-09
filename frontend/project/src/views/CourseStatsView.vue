<!-- frontend/src/views/FeedbackComponent.vue -->

<template>
    <div class="feedback-container">
        <h1><strong>Stats for </strong> {{ courseName }}</h1>
        <p>Course ID{{ courseCode }}</p>
        <div v-if="statsData.average_rating" class="feedback-list">
            <!-- Customize this part based on the structure of your feedback data -->
            <p><strong>Average Rating:</strong> {{ statsData.average_rating }}</p>
            <p><strong>Number of students completed the course:</strong> {{ statsData.n_students }}</p>
            <!-- Add more fields as needed -->
        </div>
        <div v-else class="no-feedback-message">
            <p>No stats available for this course.</p>
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
            courseName: '',
            statsData: '',
        };
    },
    created() {
        // Access the course_code parameter from the route
        this.courseCode = this.$route.params.course_code;

        // Fetch stats data using the course_code
        this.fetchStats();
    },
    methods: {
        async fetchStats() {
            try {
                const response = await fetch(`http://localhost:8000/course/stats/course/${this.courseCode}`);
                const data = await response.json();
                console.log(data);
                this.statsData = data;
                this.courseName = data.course_name;
                console.log(this.statsData);
            } catch (error) {
                console.error('Error fetching course stats:', error);
                this.statsData = 'Error fetching course stats.';
            }
        },
    }
};
</script>
    