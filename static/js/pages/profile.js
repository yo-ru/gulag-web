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
        }
    },
    created() { 
        var vm = this;
        window.history.replaceState('', document.title, "/u/" + vm.mode + "/" + vm.mods + "/" + vm.userid);
        vm.LoadProfileData(vm.userid)
        vm.LoadMostBeatmaps(vm.userid, vm.mode, vm.mods)
        vm.LoadScores(vm.userid, vm.mode, vm.mods, 'best')
        vm.LoadScores(vm.userid, vm.mode, vm.mods, 'recent')
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
                mods: mods
            }})
            .then(function(response){
                vm.mostdata = response.data;
            });
        },
        LoadScores(userid, mode, mods, sort) {
            var vm = this;
            vm.$axios.get("http://" + window.location.hostname + ":" + window.location.port + "/api/get_scores", { params: { 
                id: userid, 
                mode: mode,
                mods: mods,
                sort: sort
            }})
            .then(function(response){
                vm[`${sort}data`] = response.data;
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
            window.history.replaceState('', document.title, "/u/" + vm.mode + "/" + vm.mods + "/" + vm.userid);
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