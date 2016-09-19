import base
import random

class BooleanSample(base.Sample):
    def __init__(self):
        self.gen = None
    def genDis(self, resultingDistribution=[0.5,0.5], count=0):
        #ensure that the sum of each result occurs a certain
        #percent of time. This ensures the distribution and
        #is not a probability
        op_count = [0, 0]
        end_dist = [count*resultingDistribution[0], count*resultingDistribution[1]]
        remaining = count
        for i in range(count):
            r = False
            if op_count[0] == end_dist[0]:
                r = False
            elif op_count[1] == end_dist[1]:
                r = True
            else:
                r = bool(random.getrandbits(1))

            if r:
                op_count[0] = op_count[0] + 1
            else:
                op_count[1] = op_count[1] + 1
            yield r

    def sample(self, size, field, spec=None):
        choices = ChoiceDistribution.objects.filter(field=spec)
        if self.gen == None and spec==None:
            return bool(random.getrandbits(1))
        elif self.gen == None and spec != None and len(choices) > 0:
            true_choice = choices.filter(value="TRUE")
            false_choice = choices.filter(value="FALSE")
            resultingDistribution = [0.0, 0.0]
            gen_dis = False
            if len(true_choice) > 0 and true_choice[0].ensure_distribution:
                resultingDistribution[0] = true_choice[0].distribution
                gen_dis = True
            if len(false_choice) > 0 and false_choice[0].ensure_distribution:
                resultingDistribution[1] = false_choice[0].distribution
                gen_dis = True
            if gen_dis:
                self.gen = self.genDis(resultingDistribution, size)

        r = False
        if self.gen != None:
            r = next(self.gen)
        else:
            r = bool(random.getrandbits(1))

        return r
