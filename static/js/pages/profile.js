new Vue({
    el: "#profile",
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
            limit: [5, 5, 5],
            full: [false, false, false]
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
            vm.$axios.get("https://" + window.location.hostname + ":" + window.location.port + "/api/get_user", {
                params: {
                    id: userid,
                }
            })
                .then(function (response) {
                    vm.userdata = response.data;
                });
        },
        LoadMostBeatmaps(userid, mode, mods) {
            var vm = this;
            vm.$axios.get("https://" + window.location.hostname + ":" + window.location.port + "/api/get_most_beatmaps", {
                params: {
                    id: userid,
                    mode: mode,
                    mods: mods,
                    limit: vm.limit[2]
                }
            })
                .then(function (response) {
                    vm.mostdata = response.data;
                    if (vm.mostdata.length != vm.limit[2]) {
                        vm.full[2] = true
                    }
                });
        },
        LoadScores(userid, mode, mods, sort) {
            var vm = this;
            switch (sort) {
                case 'best':
                    limitdata = 0
                    break;
                case 'recent':
                    limitdata = 1
                    break;
                default:
            }
            vm.$axios.get("https://" + window.location.hostname + ":" + window.location.port + "/api/get_scores", {
                params: {
                    id: userid,
                    mode: mode,
                    mods: mods,
                    sort: sort,
                    limit: vm.limit[limitdata]
                }
            })
                .then(function (response) {
                    vm[`${sort}data`] = response.data;
                    if (vm[`${sort}data`].length != vm.limit[limitdata]) {
                        if (sort == 'best') {
                            vm.full[0] = true
                        } else if (sort == 'recent') {
                            vm.full[1] = true
                        }
                    } else {
                        if (sort == 'best') {
                            vm.full[0] = false
                        } else if (sort == 'recent') {
                            vm.full[1] = false
                        }
                    }
                });
        },
        LoadGrades(userid, mode, mods) {
            var vm = this;
            vm.$axios.get("https://" + window.location.hostname + ":" + window.location.port + "/api/get_grade", {
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
                    document.getElementById('contentmodal').innerHTML = "<div class='score-beatmap'><h1 class='score-beatmap-title'><a class='score-beatmap-linkplain'>" + replaydata.artist + " - " + replaydata.title + " [" + replaydata.version + "] + "+replaydata.mods_readable +"</a></h1></div><div class='score-info'><div class='infoitem infoitem-player'><div class='score-player'><div class='score-player-row--score'> <div class='score-player-score'>" + replaydata.score + "</div></div><div class='score-player-row--player'><span>Played by</span><strong>" + replaydata.name + "</strong><span>Submitted</span><strong>" + replaydata.play_time + "</strong></div></div></div><div class='infoitem infoitem--dial'> <div class='score-dial'> <div class='score-dial-layer--grade'><span>" + replaydata.grade + "</span></div></div></div></div><div class='score-stats'> <div class='score-stats-group score-stats-group--stats'> <div class='score-stats-group-row'> <div class='score-stats-stat'> <div class='score-stats-stat-row--label'>Accuracy</div><div class='score-stats-stat-row'>" + replaydata.acc.toFixed(2) + "%</div></div><div class='score-stats-stat'> <div class='score-stats-stat-row--label'>Max Combo</div><div class='score-stats-stat-row'>" + replaydata.max_combo + "x</div></div><div class='score-stats-stat'> <div class='score-stats-stat-row--label'>pp</div><div class='score-stats-stat-row'><span>" + replaydata.pp.toFixed() + "</span></div></div></div><div class='score-stats-group-row'> <div class='score-stats-stat'> <div class='score-stats-stat-row--label'>300</div><div class='score-stats-stat-row'>" + replaydata.n300 + "</div></div><div class='score-stats-stat'> <div class='score-stats-stat-row--label'>100</div><div class='score-stats-stat-row'>" + replaydata.n100 + "</div></div><div class='score-stats-stat'> <div class='score-stats-stat-row--label'>50</div><div class='score-stats-stat-row'>" + replaydata.n50 + "</div></div><div class='score-stats-stat'> <div class='score-stats-stat-row--label'>miss</div><div class='score-stats-stat-row'>" + replaydata.nmiss + "</div></div></div></div></div>"
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