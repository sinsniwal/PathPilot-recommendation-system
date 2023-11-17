import random


class Model:
    def __init__(self):
        self.foundation_courses_1 = ["BSMA1001", "BSMA1002", "BSCS1001", "BSHS1001"]
        self.foundation_courses_2 = ["BSMA1003", "BSMA1004", "BSCS1002", "BSHS1002"]
        self.diploma_courses_1 = [
            "BSCS2001",
            "BSCS2002",
            "BSCS2003",
            "BSCS2005",
            "BSSE2001",
        ]
        self.diploma_courses_2 = ["BSCS2006"]
        self.diploma_courses_3 = ["BSCS2004", "BSMS2001", "BSCS2007", "BSSE2002"]
        self.diploma_courses_4 = ["BSCS2008", "BSMS2002"]
        self.degree_courses_1 = [
            "BSCS3001",
            "BSCS3002",
            "BSGN3001",
            "BSCS3003",
            "BSCS3004",
        ]
        self.degree_courses_2 = [
            "BSBT4001",
            "BSBT4002",
            "BSCS3005",
            "BSCS4001",
            "BSEE4001",
            "BSMS3001",
            "BSMS4001",
            "BSCS4004",
            "BSMS3002",
            "BSCS3007",
            "BSCS3006",
            "BSGN3002",
            "BSMA3012",
            "BSCS4021",
            "BSMA3014",
            "BSCS3005",
            "BSMA2001",
        ]
        self.degree_courses_3 = ["BSCS4002", "BSCS4003", "BSCS3031"]

    def predict(self, completed_courses):
        all_courses = (
            random.sample(self.foundation_courses_1, len(self.foundation_courses_1))
            + random.sample(self.foundation_courses_2, len(self.foundation_courses_2))
            + random.sample(self.diploma_courses_1, len(self.diploma_courses_1))
            + random.sample(self.diploma_courses_2, len(self.diploma_courses_2))
            + random.sample(self.diploma_courses_3, len(self.diploma_courses_3))
            + random.sample(self.diploma_courses_4, len(self.diploma_courses_4))
            + random.sample(self.degree_courses_1, len(self.degree_courses_1))
            + random.sample(self.degree_courses_2, len(self.degree_courses_2))
            + random.sample(self.degree_courses_3, len(self.degree_courses_3))
        )
        all_courses = [
            course for course in all_courses if course not in completed_courses
        ]
        return all_courses[: (34 - len(completed_courses))]
