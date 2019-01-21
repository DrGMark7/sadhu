import mongoengine as me
import datetime


class Assignment(me.Document):
    name = me.StringField(required=True)
    description = me.StringField(required=True)
    score = me.IntField(required=True, default=0)
    tags = me.ListField(me.StringField(required=True))
    course = me.ReferenceField('Course',
                               dbref=True,
                               required=True)

    # started_date = me.DateTimeField(required=True,
    #                                 default=datetime.datetime.now)
    # ended_date = me.DateTimeField(required=True,
    #                               default=datetime.datetime.now)

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.now)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.now,
                                    auto_now=True)

    challenges = me.ListField(
            me.ReferenceField('Challenge',
                              db_ref=True,
                              required=True))

    owner = me.ReferenceField('User', db_ref=True, required=True)
    contributors = me.ListField(
            me.ReferenceField('User',
                              dbref=True,
                              required=True))

    meta = {'collection': 'assignments'}

    def get_solutions(self, user, class_):
        from sadhu import models
        solutions = models.Solution.objects(
                owner=user,
                enrolled_class=class_,
                challenge__in=self.challenges)


        return solutions

    def get_score(self, class_, user):
        from sadhu import models
        solutions = models.Solution.objects(
                owner=user,
                enrolled_class=class_,
                challenge__in=self.challenges)

        best_solutions = dict()
        for s in solutions:

            if s.challenge.id in best_solutions:
                if best_solutions[s.challenge.id]['score'] < s.score:
                    best_solutions[s.challenge.id]['score'] = s.score
            else:
                best_solutions[s.challenge.id] = dict(
                        challenge=s.challenge,
                        score=s.score)

        total_assignment_score = sum(
                [d['challenge'].score for d in best_solutions.values()])
        total_solution_score = sum(
                [d['score'] for d in best_solutions.values()])

        score = 0
        if total_assignment_score != 0:
            score = total_solution_score/total_assignment_score * self.score

        return score


    def check_user_submission(self, class_, user):
        from sadhu import models

        challenge_checker = dict()
    
        solutions = models.Solution.objects(
                owner=user,
                enrolled_class=class_,
                challenge__in=self.challenges)

        for s in solutions:
            challenge_checker[s.challenge.id] = s.status

        return challenge_checker


