class DataApi():
    LABEL_TO_GENRE = {
        "ComputerVision": "cv",
        "NLP": "nlp",
        "Dialogue": "nlp",
        "Summarization": "nlp",
        "Optimization": "opt",
        "ReinforcementLearning": "rl",
        "AudioRecognition": "audio",
        "AudioSynthesis": "audio"
    }

    @classmethod
    def labels_to_genres(cls, labels):
        genres = ["" if lb not in cls.LABEL_TO_GENRE else cls.LABEL_TO_GENRE[lb] for lb in labels]
        genres = [g for g in genres if g]
        return genres

    def get_recent(self, user_id="", limit=-1):
        """
        Get Recent Posts

        Args:
            user_id: to filter the records by user_id
            limit: to filter the record count
        Returns:
            posts: array of post (post have to have "genre" filed that determined by LABEL_TO_GENRE)
                   the record is sorted by created_at (desc)
        """
        raise Exception("Have to implements in DataApi subclass.")

    def get_qualified(self, user_id="", limit=-1):
        """
        Get Qualified

        Args:
            user_id: to filter the records by user_id
            limit: to filter the record count
        Returns:
            posts: array of post (post have to have "genre" filed that determined by LABEL_TO_GENRE)
                   the record is sorted by score (desc)
        """
        raise Exception("Have to implements in DataApi subclass.")

    def aggregate_per_month(self, user_id="", month=6, use_genre=True):
        """
        Get aggreagation of post count per year_month and genre or label

        Args:
            user_id: to filter the records by user_id
            month: to limit the aggrecation time range
            use_genre: use genre to aggregate (when False then use label)
        Returns:
            aggregation: post count aggregation by year/month, genre(or label).
            example {"2017/01": {"genre1": 1, "genre2": 3, ...}}
            (The size of each year/month aggregation should be equal. 
            You have to compensate 0 if the specific genres don't exist in that year/month.)
        """
        raise Exception("Have to implements in DataApi subclass.")

    def aggregate_kinds(self, user_id="", month=6, use_genre=True):
        """
        Get aggreagation of post count per genre or label

        Args:
            user_id: to filter the records by user_id
            month: to limit the aggrecation time range
            use_genre: use genre to aggregate (when False then use label)
        Returns:
            aggregation: post count aggregation by genre(or label).
            example {"genre1": 11, "genre2": 31, ...}
        """
        raise Exception("Have to implements in DataApi subclass.")

    def get_user_total_score(self, user_id):
        raise Exception("Have to implements in DataApi subclass.")

    def get_user_post_count(self, user_id):
        raise Exception("Have to implements in DataApi subclass.")
