<template>
    <div class="row flex-lg-row align-items-top py-5 gx-0 px-5" style="min-height: 80vh;">

        <div class="col-lg-3 p-3 d-flex flex-column align-items-center" style="background-color: #cae7d8;">
            <div class="mb-5 d-flex flex-column align-items-center" style="width: 100%;">
                <h5 class="mb-5">History</h5>
                <div class="d-flex flex-column align-items-center" style="width: 100%;">
                    <div v-for="(history, index) in recommendationHistory" :key="index" class="mb-1" style="background-color: #84caa6; width: 100%; text-align:center; cursor:pointer; border: 2px solid #72b191" v-on:click="getHistory(history)">
                        <i>Recommendation {{ index + 1 }}</i>
                    </div>
                </div>
            </div>
            <div class="mb-2">
                <button type="button" class="btn btn-primary" style="background-color: #1A2E35;" v-on:click="getRecommendation">Suggest Roadmap</button>
            </div>
            <div>
                <button type="button" class="btn btn-primary" style="background-color: #801f1f; border: none" v-on:click="clearHistory">Clear History</button>
            </div>
        </div>

        <div class="col-lg-9 p-3 d-flex justify-content-center align-items-center" style="background-color: #e3f3ec;">
            <form :style="{ display: displayRecommendation ? 'none':'block' }">
                <div class="mb-3">
                  <label for="exampleInputEmail1" class="form-label">What's your goal?</label>
                  <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
                  <div id="emailHelp" class="form-text">We'll never share your personal details with anyone else.</div>
                </div>
                <div class="mb-3">
                  <label for="Commitment" class="form-label">Commitment (in hrs)</label>
                  <input type="number" class="form-control" id="commitment">
                </div>
                <button type="button" class="btn btn-primary" style="background-color: #1A2E35;" v-on:click="getRecommendation">Get Recommendation</button>
            </form>
        
            <div :style="{ display: displayRecommendation ? 'block':'none' }">
                <div class="d-flex flex-column"  v-for="(courseList, level) in displayRoadmap" :key="level">
                    <div class="d-flex justify-content-center m-2">
                        <button type="button" class="btn btn-primary text-capitalize" style="background-color: #1c353e;">{{ level }} Level</button>
                    </div>
                    <div class="d-flex flex-wrap justify-content-center mb-4">
                        <div v-for="(course, index) in courseList" :key="index">
                            →<button type="button" class="btn btn-primary m-2" style="background-color: #148ab5;" v-on:click="goCoursePage(course)">{{ getCourseName(course) }} ({{ course }})</button>
                        </div>
                    </div>
                </div>
                <div class="fw-bold" style="text-align:center">
                    NOTE: Please take care of the prerequisites and co-requisites among the courses.
                </div>
            </div>
        </div>
        
    </div>

</template>

<script setup>
import router from '@/router';
import { onMounted, ref } from 'vue';


    const roadmap = ref([])
    const displayRecommendation = ref(false)
    const displayRoadmap = ref({
        foundation: [],
        diploma: [],
        degree: [],
    })

    const recommendationHistory = ref([])

    const courses = {
        foundation: ["BSMA1001", "BSMA1002", "BSCS1001", "BSHS1001", "BSMA1003", "BSMA1004", "BSCS1002", "BSHS1002"],
        diploma: ["BSCS2001", "BSCS2002", "BSCS2003", "BSCS2005", "BSSE2001", "BSCS2006", "BSCS2004", "BSMS2001", "BSCS2007", "BSSE2002", "BSCS2008", "BSMS2002"],
        degree: ["BSCS3001", "BSCS3002", "BSGN3001", "BSCS3003", "BSCS3004",
            "BSBT4001",
            "BSBT4002",
            "BSCS3005",
            "BSCS4001",
            "BSEE4001",
            "BSMS3001",
            "BSMS4001",
            "BSCS4004",
            "BSMS3002",
            "BSCS3007",
            "BSCS3006",
            "BSGN3002",
            "BSMA3012",
            "BSCS4021",
            "BSMA3014",
            "BSMA2001","BSCS4002", "BSCS4003", "BSCS3031"],
    }

    const courseMapping = {
        'BSMA1001': 'Mathematics-1',
        'BSMA1002': 'Statistics-1',
        'BSCS1001': 'Computational Thinking',
        'BSHS1001': 'English-1',
        'BSMA1003': 'Mathematics-2',
        'BSMA1004': 'Statistics-2',
        'BSCS1002': 'Python',
        'BSHS1002': 'English-2',
        'BSCS2001': 'DBMS',
        'BSCS2002': 'PDSA',
        'BSCS2003': 'MAD-1',
        'BSCS2005': 'Java',
        'BSCS2006': 'MAD-2',
        'BSSE2001': 'System Commands',
        'BSCS2004': 'MLF',
        'BSMS2001': 'BDM',
        'BSCS2007': 'MLT',
        'BSCS2008': 'MLP',
        'BSMS2002': 'BA',
        'BSSE2002': 'TDS',
        'BSCS3002': 'Software Testing',
        'BSCS3001': 'Software Engineering',
        'BSCS3003': 'AI',
        'BSCS3004': 'Deep Learning',
        'BSGN3001': 'SPG',
        'BSBT4001': 'ATB',
        'BSBT4002': 'BDBN',
        'BSCS3005': 'C',
        'BSCS4001': 'DVD',
        'BSCS4002': 'Reinforcement Learning',
        'BSCS4003': 'Thematic Ideas in DS',
        'BSEE4001': 'Speech Tehcnology',
        'BSMS3001': 'Design Thinking',
        'BSMS4001': 'Industry 4.0',
        'BSCS4004': 'SDM',
        'BSMS3002': 'MR',
        'BSCS3007': 'PSOSM',
        'BSCS3006': 'Big Data',
        'BSGN3002': 'Financial Forensics',
        'BSMA3012': 'LSM',
        'BSCS4021': 'AA',
        'BSMA3014': 'Statistical Computing',
        'BSCS3031': 'CSD',
        'BSMA2001': 'Mathematical Thinking'
    }

    const token = ref('');
    async function getRecommendation() {

        displayRecommendation.value = true
        displayRoadmap.value = {
            foundation: [],
            diploma: [],
            degree: [],
        }

        try {
            const req = await fetch("http://localhost:8000/course/recommend", {
                method: "GET",
                headers: {
                    'Authorization': `Bearer ${token.value}`,
                }
            })
    
            if (req.status == 200) {    
                const res = await req.json()
                roadmap.value = res["roadmap"]
            } else {
                console.error("HTTPError with status code", req.status)
            }
            
            levelCourses(roadmap.value)
            recommendationHistory.value.push(roadmap.value)
            localStorage.setItem('recommendationHistory'+sessionStorage.getItem('username'), JSON.stringify(recommendationHistory.value))

        } catch(error) {
            console.error(error)
        }
    }

    // function levelCourses return a map containing keys as levels and values as coursecodes from the obtained roadmap
    function levelCourses(roadmap) {
        for (let course of roadmap) {
            if (courses.foundation.includes(course)){
                displayRoadmap.value.foundation.push(course)
            }

            if (courses.diploma.includes(course)){
                displayRoadmap.value.diploma.push(course)
            }

            if (courses.degree.includes(course)){
                displayRoadmap.value.degree.push(course)
            }
        }
    }

    function getCourseName(coursecode) {
        return courseMapping[coursecode]
    }

    // implementing history and getting token
    onMounted(() => {

        const userToken = sessionStorage.getItem('token')
        if (userToken == null) {
            router.push('/')
        }

        token.value = userToken

        const storedHistory = localStorage.getItem('recommendationHistory'+sessionStorage.getItem('username'));
        if (storedHistory) {
            recommendationHistory.value = JSON.parse(storedHistory);
            console.log(recommendationHistory.value)
        }

    })

    // function clearHistory clears the history from local storage
    function clearHistory() {
        localStorage.removeItem('recommendationHistory'+sessionStorage.getItem('username'))
        recommendationHistory.value = []
    }

    function getHistory(history) {

        displayRecommendation.value = true
        displayRoadmap.value = {
            foundation: [],
            diploma: [],
            degree: [],
        }

        levelCourses(history)
        console.log(history)
    }

    function goCoursePage(courseCode) {
        router.push({name: 'course', params: {'course_code': courseCode}})
    }

</script>