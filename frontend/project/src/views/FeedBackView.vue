<template>
  <div class=" p-7 justify-content-center align-items-center" v-on="selectedCourse" :class="{'d-flex justify-content-center align-items-center': selectedCourse==null}">
    <div class="row">
        <div      v-on="selectedCourse"  :class="{'col-md-6 mb-3': selectedCourse}">
      <form  style="padding: 30px;   background-color: #e3f3ec;">

          <p v-if="errorMessage" class="error-message" style="color: red;">{{ errorMessage }}</p>
          <div  class="mb-3" >
                <label for="courses" class="form-label">Courses</label>

                <select id="courses" class="form-select" v-model="selectedCourse" @change="handleCourseSelection">
                  <option v-for="course in courses" :key="course[0]">
                    {{ course[0] }} : {{ course[1] }}
                  </option>
                </select>
                
            </div>
            
            <div v-if="selectedCourse">
              <!-- get the course code that is selected and then  -->


              <div class="row">
                  <div class="col-md-6 mb-3">
                      <label for="title" class="form-label">Title</label>
                      <input v-model="title" type="title" class="form-control" id="title" aria-describedby="titleHelp" value="{{ mytitle }}">
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="rating" class="form-label">Rating</label>

                    <div class="rating-stars">
                        <span v-for="star in 5" :key="star" v-on="rating" @click="setRating(star)" :class="{ 'light': star <= rating }" :style="{ color: star <= rating ? 'green' : '' }">
                          &#9733;
                        </span> <strong>{{ rating }}</strong>
                    </div>
                  </div>
              </div>


              <div class="row">
                <label for="description" class="form-label">Feedback Description</label>
                <textarea v-model="description" class="form-control" id="desc" aria-describedby="descHelp" rows="5"></textarea>
              </div>
              <div class="row" v-if="myfeedback">
                <div class="col-md-6 ">
                  <button type="button" class="btn btn-primary"  style="    margin-top: 20px;background-color: #85ce9c;" v-on:click="editFeedback">Edit</button>
                </div>
                <div class="col-md-6">
                  <button type="button" class="btn btn-primary"  style="    margin-top: 20px;background-color: #ce8585;" v-on:click="deleteFeedback">Delete</button>
                </div>
              </div>
            <div class="row" v-else>
              
                <button type="button" class="btn btn-primary"  style="    margin-top: 20px;background-color: #85ce9c;" v-on:click="addFeedback">Add</button>
                </div>
            </div>



          </form>
        </div>
        <div v-if="selectedCourse" class="col-md-6 mb-3">
          
          <div v-for="feedback in feedbackData.feedbacks" :key="feedback.id">

            <div class="card" style="margin-bottom: 20px;">
                <div class="card-body" style="text-align: left;background-color:#c9eff8;"    >
                  <div class="row" >
                  <div class="col">
                    <span style="font-size: 20px">{{ feedback.title }}</span>
                  </div>
                  <div class='col'>
                    <div class="rating-stars">
                      <span v-for="star in feedback.rating" :key="star" class="star" :class="{ 'light': star <= feedback.rating }">
                        &#9733;
                      </span>
                      <strong>{{ feedback.rating }}</strong>
                    </div>
                  </div></div>
                  
                    <div class="row">
                        <div class="col-md-10" >
                            <p>
                                <strong>{{ feedback.student_username }}</strong>

                          </p>
                          <hr>
                          <div class="clearfix"></div>
                            <p>{{feedback.description}}</p>
                            <p>
                          </p>
                        </div>
                    </div>
                      
                            </div>
                        </div>

              </div>

        </div>
        <div v-else>
            Please select course to see/edit feedbacks.
      </div>
    </div>
  </div>

      <!--
  <div class="feedback-container">
    <h1><strong>Feedback for </strong> {{ courseName }}</h1>
    <p>Course ID{{ courseCode }}</p>
    <div v-if="feedbackData.feedbacks && feedbackData.feedbacks.length > 0" class="feedback-list">
      <div v-for="feedback in feedbackData.feedbacks" :key="feedback.id" class="feedback-item">
        <p><strong>Title:</strong> {{ feedback.title }}</p>
        <p><strong>Rating:</strong> {{ feedback.rating }}</p>
        <p><strong>Description:</strong> {{ feedback.description }}</p>
      </div>
    </div>
    <div v-else class="no-feedback-message">
      <p>No feedback available for this course.</p>
    </div>
  </div>
-->
</template>


<style scoped>
.feedback-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}
.light{
                        color:'green',
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
        selectedCourse: null,
        courseCode: '',
        feedbackData: '',
        courseName: '',
        courses: [],
        token: sessionStorage.getItem('token'),
        rating:"",
        myfeedback:null,
        username: sessionStorage.getItem('username'),
        title:"",
        description:"",
        userToken:null
      };
    },
    created() {
      // Access the course_code parameter from the route
      this.courseCode = this.$route.params.course_code;
  
      // Fetch feedback data using the course_code
      this.rating="";
      this.courses= this.getCourses();
      this.userToken = sessionStorage.getItem('token')
    },
    methods: {




      async handleCourseSelection()
      {
        this.myfeedback=null;
        this.title=null;
        this.rating=null;
        this.description=null;
        
        let code = this.selectedCourse.split(" ")[0];
        this.courseid=code;
        this.feedbackData=await this.fetchFeedback(code);
        let a=this.feedbackData["feedbacks"];
        for (let i = 0; i < a.length; i++) {
            const element = a[i];
            if (element["student_username"]==this.username) {
                this.myfeedback=element; 
                this.title=this.myfeedback['title']
                this.rating=this.myfeedback['rating']
                this.description=this.myfeedback['description']
          }
          }
      },
      
      setRating(a) {
        this.rating=a;
        // Add your code here to handle the rating
      },

      async editFeedback() {
            try {
                const tok=sessionStorage.getItem('token')
                // Send request to server to register user
                const response = await fetch(`http://127.0.0.1:8000/course/feedback/modify/${this.myfeedback['fid']}`, {
                    method: 'POST',
                    headers: {
                      'Authorization': `Bearer ${tok}`,
                      'Content-Type': 'application/json'
                    
                    },
                    body: JSON.stringify({
                        rating: this.rating,
                        title: this.title,
                        description: this.description,
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    if(data.message=="Feedback saved successfully"){
                            // Redirect to home page
                            location.reload();
                        } 
                    } else {
                            this.errorMessage = "permission denied!";
                    }
            } catch (error) {
                this.errorMessage = 'An error occurred during registration:';
            }
        },

      async deleteFeedback() {
            try {
                const tok=sessionStorage.getItem('token')
                // Send request to server to register user
                const response = await fetch(`http://127.0.0.1:8000/course/feedback/modify/${this.myfeedback['fid']}`, {
                    method: 'DELETE',
                    headers: {
                      'Authorization': `Bearer ${tok}`
                    
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    if(data.message=="Feedback deleted successfully"){
                            // Redirect to home page
                            location.reload();
                        } 
                    } else {
                            this.errorMessage = "permission denied!";
                    }
            } catch (error) {
                this.errorMessage = 'An error occurred during registration:';
            }
        },
      async addFeedback() {
            try {
                const tok=sessionStorage.getItem('token')
                // Send request to server to register user
                const response = await fetch(`http://127.0.0.1:8000/course/feedback/`, {
                    method: 'POST',
                    headers: {
                      'Authorization': `Bearer ${tok}`,
                      'Content-Type': 'application/json'
                    
                  },
                  body: JSON.stringify({
                        course_code:this.courseid,
                        rating: this.rating,
                        title: this.title,
                        description: this.description,
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    if(data.message=="Feedback saved successfully"){
                            // Redirect to home page
                            location.reload();
                        } 
                    } else {
                            this.errorMessage = "permission denied!";
                    }
            } catch (error) {
                this.errorMessage = 'An error occurred during registration:';
            }
        },
      async fetchFeedback(courseode) {
        try {
          const response = await fetch(`http://localhost:8000/course/feedback/${courseode}`);
          const data = await response.json();
          this.feedbackData = data;
          this.courseName = data.course_name;
          console.log(this.feedbackData);
        } catch (error) {
          console.error('Error fetching feedback:', error);
          this.feedbackData = 'Error fetching feedback.';
        }
        return this.feedbackData
      },
      async getCourses() {
        try {
            const req = await fetch("http://localhost:8000/course/recommend", {
                method: "GET",
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                }
            })

            if (req.status == 200) {    
                const res = await req.json()
                this.courses = res["completed_courses_names"]
            } else {
                console.error("HTTPError with status code", req.status)
            }
        } catch(error) {
            console.error(error)
        }
      }
    },
  };
  </script>
  