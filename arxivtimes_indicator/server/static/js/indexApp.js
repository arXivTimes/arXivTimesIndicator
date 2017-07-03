var instance = new Vue({
    el: "#app",
    delimiters: ["[[", "]]"],
    data: {
        papers: PAPERS,
        selected: "all",
        isRecent: true,
        labelToGenre: LABEL_TO_GENRE,
        genreNames: GENRE_NAMES
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
            if (this.selected in this.genreNames){
                return this.genreNames[this.selected];
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
            var targetLabel = this.labelToGenre[this.selected];
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
            var date = v.replace(/T|Z/g, " ").split(" ");
            return date[0];
        }
    }
})
