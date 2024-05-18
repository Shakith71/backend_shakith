new Vue({
    el: '#app',
    data: {
        theaters: []  // Initialize theaters data
    },
    mounted() {
        // Fetch theaters data from Flask route
        fetch('/theaters')
            .then(response => response.json())
            .then(data => {
                this.theaters = data;
            });
    }
});
