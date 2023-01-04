from experta import *


class Cases(Fact):
    confirmed = Field(int, default=0)
    hospitalized = Field(int, default=0)
    deathRate = Field(int, default=0)
    healedRate = Field(int, default=0)


class NewDailyCases(Fact):
    pass


class AvailableHospitalBed(Fact):
    available = Field(int, default=0)
    occupied = Field(int, default=0)


class QuarantineClassifier(KnowledgeEngine):
    # death rate = death / confirmed * 100%
    # death rate = 0% [0]
    @Rule(AND(
        Cases(deathRate=0),
        Cases(healedRate=90)
    ))
    def level0(self):
        print("Quarantine Level 0")

    # death rate <= 10% [1]
    @Rule(AND(
        Cases(deathRate=10),
        Cases(healedRate=80)
    ))
    def level1(self):
        print("Quarantine Level 1")

    # death rate <= 20% [2]
    @Rule(AND(
        Cases(deathRate=20),
        Cases(healedRate=70)
    ))
    def level2(self):
        print("Quarantine Level 2")

    # death rate <= 40% [3]
    @Rule(AND(
        Cases(deathRate=40),
        Cases(healedRate=50)
    ))
    def level3(self):
        print("Quarantine Level 3")

    # death rate > 40% [4]
    @Rule(AND(
        Cases(deathRate=100),
        Cases(healedRate=0)
    ))
    def level4(self):
        print("Quarantine Level 4")

    # healed rate = healed / hospitalized * 100
    # healed rate >= 90% [0]
    # healed rate >= 80% [1]
    # healed rate >= 70% [2]
    # healed rate >= 50% [3]
    # healed rate < 50& [4]

    # occupied bed ratio = occupied / (occupied + available)
    # occupied bed ratio >= 40% need quarantine


def scaleDeathRate(death_cases, _cases):
    defDeathRate = int(int(death_cases) / int(_cases) * 100)

    # scaling death rate to fulfil conditions
    if defDeathRate <= 5:
        defDeathRate = 0
    elif defDeathRate <= 10:
        defDeathRate = 10
    elif defDeathRate <= 20:
        defDeathRate = 20
    elif defDeathRate <= 40:
        defDeathRate = 40
    else:
        defDeathRate = 100

    return defDeathRate


def scaleHealedRate(healed_cases, hospitalized_cases):
    defHealedRate = int(int(healed_cases)/int(hospitalized_cases))

    # scaling healed rate to fulfil conditions
    if defHealedRate >= 90:
        defHealedRate = 90
    elif defHealedRate >= 80:
        defHealedRate = 80
    elif defHealedRate >= 70:
        defHealedRate = 70
    elif defHealedRate >= 50:
        defHealedRate = 50
    else:
        defHealedRate = 0

    return defHealedRate


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    engine = QuarantineClassifier()
    engine.reset()

    cases = input("Number of Cases: ")
    hospitalizedCases = input("Number of Hospitalized: ")
    healedCases = input("Number of Healed: ")
    deathCases = input("Number of Deaths: ")

    healedRate = scaleHealedRate(healedCases, hospitalizedCases)
    deathRate = scaleDeathRate(deathCases, cases)

    engine.declare(Cases(deathRate=deathRate, healedRate=healedRate))
    engine.run()
