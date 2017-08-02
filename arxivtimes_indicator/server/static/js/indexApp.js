var instance = new Vue({
    el: "#app",
    delimiters: ["[[", "]]"],
    data: {
        posts: POSTS,
        selected: "all",
        isRecent: true,
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
        },
        pocketLink: function(post){
            return "https://getpocket.com/edit.php?url=" + post.url + "&title=" + post.title;
        }
    },
    computed: {
        title: function(){
            if (this.selected in this.genreNames){
                return this.genreNames[this.selected];
            }else{
                return "All Genres";
            }
        },
        filteredList: function(){
            var listType = this.isRecent ? "recent" : "quality";
            var filtered = this.posts[listType];
            if(filtered === undefined){
                filtered = [];
            }
            if(this.selected != "all"){
                var selected = this.selected;
                var filtered = filtered.filter(function(item){
                    return item.genres.indexOf(selected) > -1 ? true : false;
                })
            }
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
