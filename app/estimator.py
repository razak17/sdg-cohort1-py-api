def convert_to_days(data):
    number_of_days = None

    if data["periodType"] == "months":
        number_of_days = data["timeToElapse"] * 30

    elif data["periodType"] == "weeks":
        number_of_days = data["timeToElapse"] * 7

    elif data["periodType"] == "days":
        number_of_days = data["timeToElapse"]

    return number_of_days


def requested_time(data):
    if data["periodType"] == "months":
        return 2 ** int((data["timeToElapse"] * 30) / 3)

    elif data["periodType"] == "weeks":
        return 2 ** int((data["timeToElapse"] * 7) / 3)

    return 2 ** int(data["timeToElapse"] / 3)


# IMPACT
def impactEstimates(data):
    # Challenge 1
    currently_infected = data["reportedCases"] * 10

    projected_infections = currently_infected * requested_time(data)

    # Challenge 2
    severe_cases_by_requested_time = int(projected_infections * 0.15)

    total_hospital_beds = data["totalHospitalBeds"] * 0.35
    available_beds = total_hospital_beds - severe_cases_by_requested_time
    available_beds = int(available_beds)

    # Challenge 3
    cases_for_ICU_by_requested_time = projected_infections * 0.05
    cases_for_ICU_by_requested_time = int(cases_for_ICU_by_requested_time)

    cases_for_ventilators_by_requested_time = projected_infections * 0.02
    cases_for_ventilators_by_requested_time = int(
        cases_for_ventilators_by_requested_time)

    avg_daily_income_USD = data["region"]["avgDailyIncomeInUSD"]
    avg_daily_income_population = data["region"]["avgDailyIncomePopulation"]
    initial = avg_daily_income_USD * avg_daily_income_population

    dollars_in_flight = (
        projected_infections * initial) / convert_to_days(data)
    dollars_in_flight = int(dollars_in_flight)

    return {
        "currentlyInfected": int(currently_infected),
        "infectionsByRequestedTime": int(projected_infections),
        "severeCasesByRequestedTime": int(severe_cases_by_requested_time),
        "hospitalBedsByRequestedTime": int(available_beds),
        "casesForICUByRequestedTime": int(cases_for_ICU_by_requested_time),
        "casesForVentilatorsByRequestedTime": int(
            cases_for_ventilators_by_requested_time),
        "dollarsInFlight": float(dollars_in_flight)
    }


# SEVERE IMPACT
def severeImpactEstimates(data):
    # Challenge 1
    currently_infected = data["reportedCases"] * 50
    projected_infections = currently_infected * requested_time(data)

    # Challenge 2
    severe_cases_by_requested_time = int(projected_infections * 0.15)

    total_hospital_beds = data["totalHospitalBeds"] * 0.35
    available_beds = int(total_hospital_beds - severe_cases_by_requested_time)

    # Challenge 3
    cases_for_ICU_by_requested_time = projected_infections * 0.05
    cases_for_ICU_by_requested_time = int(cases_for_ICU_by_requested_time)

    cases_for_ventilators_by_requested_time = projected_infections * 0.02
    cases_for_ventilators_by_requested_time = int(
        cases_for_ventilators_by_requested_time)

    avg_daily_income_USD = data["region"]["avgDailyIncomeInUSD"]
    avg_daily_income_population = data["region"]["avgDailyIncomePopulation"]
    initial = avg_daily_income_USD * avg_daily_income_population
    dollars_in_flight = (
        projected_infections * initial) / convert_to_days(data)
    dollars_in_flight = int(dollars_in_flight)

    return {
        "currentlyInfected": int(currently_infected),
        "infectionsByRequestedTime": int(projected_infections),
        "severeCasesByRequestedTime": int(severe_cases_by_requested_time),
        "hospitalBedsByRequestedTime": int(available_beds),
        "casesForICUByRequestedTime": int(cases_for_ICU_by_requested_time),
        "casesForVentilatorsByRequestedTime": int(
            cases_for_ventilators_by_requested_time),
        "dollarsInFlight": float(dollars_in_flight)
    }


def estimator(data):
    response = {
        "data": data,
        "impact": impactEstimates(data),
        "severeImpact": severeImpactEstimates(data),
    }
    return response
