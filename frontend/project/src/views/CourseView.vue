<template>
    <div class="d-flex flex-column align-items-center">
    <i><h4 class="display-7 mb-2" style="font-weight: bold">{{ course_name }} ({{ course_code }}) <span><a :href="'https://study.iitm.ac.in/ds/course_pages/' + course_code + '.html'"><img width="25" height="25" src="https://img.icons8.com/ios-glyphs/30/000000/search--v1.png" alt="search--v1"/></a></span></h4></i>

    <div class="d-flex flex-wrap p-2 mt-5 justify-content-around" style="width: 100%;">
        <div style="border: 1px solid #2a342f; width:25%; background-color: #e3f3ec;">
            <div style="background-color: #1A2E35; color:aliceblue">
                <h5>
                    Average Rating
                </h5>
            </div>
            <div>
                <h5 class>
                    {{ avg_rating }}
                </h5>
            </div>
        </div>
        <div style="border: 1px solid #2a342f; width:25%; background-color: #e3f3ec;">
            <div style="background-color: #1A2E35; color:aliceblue">
                <h5>
                    Number of students Completed this course
                </h5>
            </div>
            <div>
                <h5>
                    {{ n_students }}
                </h5>
            </div>
        </div>
    </div>
    <div class="mt-5 w-100">
        <h5 style="font-weight: bold">Feedbacks</h5>
        <div v-for="feedback in feedbacks" :key="feedback.fid" class="card mb-3">
          <div class="card-header" style="background-color: #1A2E35; color: aliceblue;">
            {{ feedback.student_roll_no }}
          </div>
          <div class="card-body">
            <div class="d-flex justify-content-around align-items-center">
              <h6 class="card-title"><i>Title</i>: {{ feedback.title }}</h6>
              <h6 class="card-subtitle mb-2 text-muted">Rating: {{ feedback.rating }}</h6>
            </div>
            <p class="card-text">{{ feedback.description }}</p>
          </div>
        </div>
    </div>
    </div>


</template>

<script setup>
import router from '@/router';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

    const course_code = ref('')
    const token = ref('')
    const $route = useRoute()

    const course_name = ref('')
    const n_students = ref(0)
    const avg_rating = ref(0.0)
    const feedbacks = ref([])

    onMounted(async () => {

        const userToken = sessionStorage.getItem('token')
        if (userToken == null) {
            router.push('/')
        }

        token.value = userToken
        course_code.value = $route.params.course_code 
          
        
        try {
            const req = await fetch("http://localhost:8000/course/stats/course/" + course_code.value, {
                method: "GET",
                headers: {
                    'Authorization': `Bearer ${token.value}`,
                }
            })
    
            if (req.status == 200) {    
                const res = await req.json()
                course_name.value = res["course_name"]
                avg_rating.value = res['average_rating']
                n_students.value = res['n_students']

            } else {
                console.error("HTTPError with status code", req.status)
            }
            

        } catch(error) {
            console.error(error)
        }

        try {
            const req = await fetch("http://localhost:8000/course/feedback/" + course_code.value, {
                method: "GET",
                headers: {
                    'Authorization': `Bearer ${token.value}`,
                }
            })
    
            if (req.status == 200) {    
                const res = await req.json()
                feedbacks.value = res['feedbacks']
                console.log(res)

            } else {
                console.error("HTTPError with status code", req.status)
            }
            

        } catch(error) {
            console.error(error)
        }
    })

</script>