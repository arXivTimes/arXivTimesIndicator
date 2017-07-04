class DataApi():
    LABEL_TO_GENRE = {
        "ComputerVision": "cv",
        "NLP": "nlp",
        "Dialogue": "nlp",
        "Optimization": "opt",
        "ReinforcementLearning": "rl",
        "AudioRecognition": "audio",
        "AudioSynthesis": "audio"
    }

    def get_recent(self, user_id="", limit=-1):
        raise Exception("Have to implements in DataApi subclass.")

    def get_popular(self, user_id="", limit=-1):
        raise Exception("Have to implements in DataApi subclass.")

    def aggregate_per_month(self, user_id="", month=6, use_genre=True):
        raise Exception("Have to implements in DataApi subclass.")

    def aggregate_kinds(self, user_id="", month=6, use_genre=True):
        raise Exception("Have to implements in DataApi subclass.")
