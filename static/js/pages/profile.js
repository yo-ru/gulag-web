new Vue({
    el: "#app",
    delimiters: ["<%", "%>"],
    data() {
        return {
            userdata: {},
            mostdata: {},
            recentdata: {},
            bestdata: {},
            gradedata: {},
            mode: mode,
            mods: mods,
            userid: userid,
            loaddata: [false, false, false]
        }
    },
    created() {
        var vm = this;
        vm.LoadProfileData(vm.userid)
        vm.LoadMostBeatmaps(vm.userid, vm.mode, vm.mods)
        vm.LoadScores(vm.userid, vm.mode, vm.mods, 'best')
        vm.LoadScores(vm.userid, vm.mode, vm.mods, 'recent')
        vm.LoadGrades(vm.userid, vm.mode, vm.mods)
        window.history.replaceState('', document.title, "/u/" + vm.userid);
    },
    methods: {
        LoadProfileData(userid) {
            var vm = this;
            vm.$axios.get(window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/api/get_user_info", {
                params: {
                    id: userid,
                }
            })
                .then(function (response) {
                    vm.userdata = response.data.userdata;
                });
        },
        LoadMostBeatmaps(userid, mode, mods) {
            var vm = this;
            vm.loaddata[2] = true
            vm.$axios.get(window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/api/get_player_most", {
                params: {
                    id: userid,
                    mode: mode,
                    mods: mods,
                    limit: 5
                }
            })
                .then(function (response) {
                    vm.mostdata = response.data.maps;
                    vm.loaddata[2] = false
                });
        },
        LoadScores(userid, mode, mods, sort) {
            var vm = this;
            switch (sort) {
                case 'best':
                    type = 0
                    vm.loaddata[0] = true
                    break;
                case 'recent':
                    type = 1
                    vm.loaddata[1] = true
                    break;
                default:
            }
            vm.$axios.get(window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/api/get_player_scores", {
                params: {
                    id: userid,
                    mode: mode,
                    mods: mods,
                    sort: sort,
                    limit: 5
                }
            })
                .then(function (response) {
                    vm[`${sort}data`] = response.data.scores;
                    if (sort == 'best') {
                        vm.loaddata[0] = false
                    } else if (sort == 'recent') {
                        vm.loaddata[1] = false
                    }
                });
        },
        LoadGrades(userid, mode, mods) {
            var vm = this;
            vm.$axios.get(window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/api/get_user_grade", {
                params: {
                    id: userid,
                    mode: mode,
                    mods: mods,
                }
            })
                .then(function (response) {
                    vm.gradedata = response.data;
                });
        },
        LoadReplay(id, mods) {
            var vm = this;
            document.getElementById('contentmodal').innerHTML = ""
            document.getElementById('modaldisplayer').className = "modal is-active"
            vm.$axios.get(window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/api/get_replay",
                {
                    params: {
                        id: id,
                        mods: mods,
                    }
                })
                .then(function (response) {
                    replaydata = response.data;
                    document.getElementById('contentmodal').innerHTML = "<div class='score-beatmap'><h1 class='score-beatmap-title'><a class='score-beatmap-linkplain'>" + replaydata.artist + " - " + replaydata.title + " [" + replaydata.version + "]</a></h1></div><div class='score-info'><div class='infoitem infoitem-player'><div class='score-player'><div class='score-player-row--score'> <div class='score-player-score'>" + replaydata.score + "</div></div><div class='score-player-row--player'><span>Played by</span><strong>" + replaydata.name + "</strong><span>Submitted on</span><strong>" + replaydata.play_time + "</strong></div></div></div><div class='infoitem infoitem--dial'> <div class='score-dial'> <div class='score-dial-layer--grade'><span>" + replaydata.grade + "</span></div></div></div></div><div class='score-stats'> <div class='score-stats-group score-stats-group--stats'> <div class='score-stats-group-row'> <div class='score-stats-stat'> <div class='score-stats-stat-row--label'>Accuracy</div><div class='score-stats-stat-row'>" + replaydata.acc + "%</div></div><div class='score-stats-stat'> <div class='score-stats-stat-row--label'>Max Combo</div><div class='score-stats-stat-row'>" + replaydata.max_combo + "x</div></div><div class='score-stats-stat'> <div class='score-stats-stat-row--label'>pp</div><div class='score-stats-stat-row'><span>" + replaydata.pp + "</span></div></div></div><div class='score-stats-group-row'> <div class='score-stats-stat'> <div class='score-stats-stat-row--label'>300</div><div class='score-stats-stat-row'>" + replaydata.n300 + "</div></div><div class='score-stats-stat'> <div class='score-stats-stat-row--label'>100</div><div class='score-stats-stat-row'>" + replaydata.n100 + "</div></div><div class='score-stats-stat'> <div class='score-stats-stat-row--label'>50</div><div class='score-stats-stat-row'>" + replaydata.n50 + "</div></div><div class='score-stats-stat'> <div class='score-stats-stat-row--label'>miss</div><div class='score-stats-stat-row'>" + replaydata.nmiss + "</div></div></div></div></div>"
                });
        },
        ChangeModeMods(mode, mods) {
            var vm = this;
            if (window.event) {
                window.event.preventDefault();
            }
            vm.mode = mode
            vm.mods = mods
            vm.LoadMostBeatmaps(vm.userid, vm.mode, vm.mods)
            vm.LoadScores(vm.userid, vm.mode, vm.mods, 'best')
            vm.LoadScores(vm.userid, vm.mode, vm.mods, 'recent')
            vm.LoadGrades(vm.userid, vm.mode, vm.mods)
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
        secondsToDhm(seconds) {
            seconds = Number(seconds);
            var d = Math.floor(seconds / (3600*24));
            var h = Math.floor(seconds % (3600*24) / 3600);
            var m = Math.floor(seconds % 3600 / 60);
            
            var dDisplay = d + "d ";
            var hDisplay = h + "h ";
            var mDisplay = m + "m ";
            return dDisplay + hDisplay + mDisplay;
        },
    },
    computed: {
    }
});
