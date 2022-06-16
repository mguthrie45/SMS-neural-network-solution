class Validator:
    def __init__(self, threshold):
        self.threshold = threshold

    def validate(self, score: float) -> bool:
        return True if score >= self.threshold else False