var instance = new Vue({
    el: "#app",
    delimiters: ["[[", "]]"],
    data: {
        papers: PAPERS,
        selected: "all",
        isRecent: true,
        labelDict: {
            "cv": ["ComputerVision"],
            "nlp": ["NLP", "Dialogue"],
            "opt": ["Optimization"],
            "rl": ["ReinforcementLearning"],
            "audio": ["AudioRecognition", "AudioSynthesis"]
        }
    },
    methods: {
        isActive: function(kind){
            return kind == this.selected ? "is-active" : "";
        },
        activate: function(kind){
            return this.selected = kind;
        },
        toggleList: function(){
            this.isRecent = !this.isRecent;
        }
    },
    computed: {
        title: function(){
            if (this.selected == "cv"){
                return "Computer Vision";
            }else if (this.selected == "nlp"){
                return "Natural Language Processing";
            }else if (this.selected == "audio"){
                return "Audio";
            }else if (this.selected == "rl"){
                return "Reinforcement Learning";
            }else if (this.selected == "opt"){
                return "Optimization";
            }else{
                return "All Genre";
            }
        },
        filteredList: function(){
            var listType = this.isRecent ? "recent" : "popular";
            var list = this.papers[listType];
            if(list === undefined){
                list = [];
            }
            var targetLabel = this.labelDict[this.selected];
            var filtered = list.filter(function(item){
                if(targetLabel === undefined){
                    return true;
                }
                var isTarget = false;
                for(var i = 0; i < targetLabel.length; i++){
                    if(item.labels.indexOf(targetLabel[i]) > -1){
                        isTarget = true;
                        break;
                    }
                }
                return isTarget;
            })
            return filtered;
        }
    },
    filters: {
        makeHeadline: function(markdText){
            var rendered = marked(markdText, { sanitize: true });
            var rendered = rendered.replace(/<\/?[^>]+(>|$)/g, "");
            return rendered;
        },
        formatDate: function (v) {
            return v.replace(/T|Z/g, ' ')
        }
    }
})

