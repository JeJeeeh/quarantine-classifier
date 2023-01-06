from experta import *


class Cases(Fact):
    confirmed = Field(int, default=0)
    hospitalized = Field(int, default=0)
    deathRate = Field(int, default=0)
    healedRate = Field(int, default=0)


class NewDailyCases(Fact):
    count = Field(int, default=0)
    status = Field(int, default=1)


class AvailableHospitalBed(Fact):
    availableRatio = Field(int, default=0)


class QuarantineClassifier(KnowledgeEngine):

    @Rule(AND(
        NewDailyCases(count=0),
        NewDailyCases(status=1),
        Cases(deathRate=0)
    ))
    def level0(self):
        print("Quarantine Level 0")

    @Rule(OR(
        Cases(deathRate=0),
        AND(
            Cases(healedRate=90),
            NewDailyCases(status=1),
            AvailableHospitalBed(availableRatio=90)
        )
    ))
    def level1(self):
        print("Quarantine Level 1")

    @Rule(OR(
        Cases(deathRate=5),
        AND(
            Cases(healedRate=75),
            NewDailyCases(status=1),
            AvailableHospitalBed(availableRatio=75)
        )
    ))
    def level2(self):
        print("Quarantine Level 2")

    @Rule(OR(
        Cases(deathRate=10),
        Cases(healedRate=40),
        NewDailyCases(status=0),
        OR(
            AvailableHospitalBed(availableRatio=30),
            AvailableHospitalBed(availableRatio=0)
        )
    ))
    def level3(self):
        print("Quarantine Level 3")

    @Rule(OR(
        Cases(deathRate=100),
        AND(
            Cases(healedRate=0),
            NewDailyCases(status=0),
            AvailableHospitalBed(availableRatio=0)
        )
    ))
    def level3(self):
        print("Quarantine Level 4")


def scaleDeathRate(death_cases, _cases):
    defDeathRate = int(int(death_cases) / int(_cases) * 100)

    # scaling death rate to fulfil conditions
    if defDeathRate <= 5:
        defDeathRate = 5
    elif defDeathRate <= 10:
        defDeathRate = 10
    else:
        defDeathRate = 100

    return defDeathRate


def scaleHealedRate(healed_cases, hospitalized_cases):
    defHealedRate = int(int(healed_cases)/int(hospitalized_cases) * 100)

    # scaling healed rate to fulfil conditions
    if defHealedRate >= 90:
        defHealedRate = 90
    elif defHealedRate >= 75:
        defHealedRate = 75
    elif defHealedRate >= 40:
        defHealedRate = 40
    else:
        defHealedRate = 0

    return defHealedRate


def getAvailableBedRatio(available_beds, occupied_beds):
    defAvailableBedRatio = int(int(available_beds)/(int(available_beds) + int(occupied_beds)))

    if defAvailableBedRatio >= 90:
        defAvailableBedRatio = 90
    elif defAvailableBedRatio >= 75:
        defAvailableBedRatio = 75
    elif defAvailableBedRatio >= 30:
        defAvailableBedRatio = 30
    else:
        defAvailableBedRatio = 0

    return defAvailableBedRatio


def getDailyStatus(daily_new_cases, available_bed):
    defDailyStatus = 0
    if int(available_bed) >= int(daily_new_cases):
        defDailyStatus = 1

    return defDailyStatus


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    engine = QuarantineClassifier()
    engine.reset()

    # getting inputs
    cases = input("Number of Cases: ")
    hospitalizedCases = input("Number of Hospitalized: ")
    healedCases = input("Number of Healed: ")
    deathCases = input("Number of Deaths: ")
    newDailyCases = input("Number of Today's New Cases: ")
    availableBeds = input("Number of Available Hospital Beds: ")
    occupiedBeds = input("Number of Occupied Hospital Beds: ")

    # get scaled inputs, ratio, and status
    healedRate = scaleHealedRate(healedCases, hospitalizedCases)
    deathRate = scaleDeathRate(deathCases, cases)
    availableBedRatio = getAvailableBedRatio(availableBeds, occupiedBeds)
    dailyStatus = getDailyStatus(newDailyCases, availableBeds)

    newDailyCases = int(newDailyCases)

    # debugging process if needed
    # print("healed rate:{healedRate}".format(healedRate=healedRate))
    # print("death rate:{deathRate}".format(deathRate=deathRate))
    # print("available bed ratio:{availableBedRatio}".format(availableBedRatio=availableBedRatio))
    # print("daily status:{dailyStatus}".format(dailyStatus=dailyStatus))

    engine.declare(
        Cases(deathRate=deathRate, healedRate=healedRate),
        NewDailyCases(status=dailyStatus, count=newDailyCases),
        AvailableHospitalBed(availableRatio=availableBedRatio)
    )
    engine.run()
