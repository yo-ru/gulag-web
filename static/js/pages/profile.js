new Vue({
    el: "#profile",
    delimiters: ["<%", "%>"],
    data() {
        return {
            userdata : {},
            mostdata : {},
            recentdata : {},
            bestdata : {},
            mode : mode,
            mods : mods,
            userid: userid,
            limit : [5,5,5],
            full: [false,false,false]
        }
    },
    created() { 
        var vm = this;
        vm.LoadProfileData(vm.userid)
        vm.LoadMostBeatmaps(vm.userid, vm.mode, vm.mods)
        vm.LoadScores(vm.userid, vm.mode, vm.mods, 'best')
        vm.LoadScores(vm.userid, vm.mode, vm.mods, 'recent')
        window.history.replaceState('', document.title, "/u/" + vm.userid);
    },
    methods: {
        LoadProfileData(userid) {
            var vm = this;
            vm.$axios.get("http://" + window.location.hostname + ":" + window.location.port + "/api/get_user", { params: { 
                id: userid, 
            }})
            .then(function(response){
                vm.userdata = response.data;
            });
        },
        LoadMostBeatmaps(userid, mode, mods) {
            var vm = this;
            vm.$axios.get("http://" + window.location.hostname + ":" + window.location.port + "/api/get_most_beatmaps", { params: { 
                id: userid, 
                mode: mode,
                mods: mods,
                limit: vm.limit[2]
            }})
            .then(function(response){
                vm.mostdata = response.data;
                if(vm.mostdata.length != vm.limit[2]) {
                    vm.full[2] = true
                }
            });
        },
        LoadScores(userid, mode, mods, sort) {
            var vm = this;
            if (sort == 'best') {
                limitdata = 0
            } else if (sort == 'recent') {
                limitdata = 1
            }
            vm.$axios.get("http://" + window.location.hostname + ":" + window.location.port + "/api/get_scores", { params: { 
                id: userid, 
                mode: mode,
                mods: mods,
                sort: sort,
                limit: vm.limit[limitdata]
            }})
            .then(function(response){
                vm[`${sort}data`] = response.data;
                if(vm[`${sort}data`].length != vm.limit[limitdata]) {
                    vm.full[limitdata] = true
                }
            });
        },
        ChangeModeMods(mode,mods) {
            var vm = this;
            if (window.event) {
                window.event.preventDefault();
            }
            vm.mode = mode
            vm.mods = mods
            vm.LoadMostBeatmaps(vm.userid, vm.mode, vm.mods)
            vm.LoadScores(vm.userid, vm.mode, vm.mods, 'best')
            vm.LoadScores(vm.userid, vm.mode, vm.mods, 'recent')
        },
        AddLimit(which) {
            var vm = this;
            if (window.event) {
                window.event.preventDefault();
            }
            if (which == 'bestscore') {
                vm.limit[0] = vm.limit[0] + 5
                vm.LoadScores(vm.userid, vm.mode, vm.mods, 'best')
            }
            else if (which == 'recentscore') {
                vm.limit[1] = vm.limit[1] + 5
                vm.LoadScores(vm.userid, vm.mode, vm.mods, 'recent')
            }
            else if (which == 'mostplay') {
                vm.limit[2] = vm.limit[2] + 5
                vm.LoadMostBeatmaps(vm.userid, vm.mode, vm.mods)
            }
        },
        addCommas(nStr) {
            nStr += '';
            var x = nStr.split('.');
            var x1 = x[0];
            var x2 = x.length > 1 ? '.' + x[1] : '';
            var rgx = /(\d+)(\d{3})/;
            while (rgx.test(x1)) {
                x1 = x1.replace(rgx, '$1' + ',' + '$2');
            }
            return x1 + x2;
        },
    },
    computed: {
    }
});