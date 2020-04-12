from marshmallow import Schema, fields, ValidationError


class region_schema(Schema):
    name = fields.String()
    avgAge = fields.Float()
    avgDailyIncomeInUSD = fields.Float()
    avgDailyIncomePopulation = fields.Float()


class estimates_schema(Schema):
    region = fields.Nested(region_schema)
    periodType = fields.String()
    timeToElapse = fields.Int()
    reportedCases = fields.Int()
    population = fields.Int()
    totalHospitalBeds = fields.Int()
